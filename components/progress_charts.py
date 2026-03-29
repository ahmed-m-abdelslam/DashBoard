import plotly.graph_objects as go
from dash import html
from config import THEME, PROJECT_COLORS
from data.utils import hex_to_rgba, status_color
from components.shared import section_title, chart_card


def make_progress_analysis(all_data):
    names = [d["project_name"] for d in all_data]
    colors = [PROJECT_COLORS[i % len(PROJECT_COLORS)]["main"] for i in range(len(all_data))]

    # Chart 1: Completion bars
    completion_fig = go.Figure()
    sorted_data = sorted(all_data, key=lambda x: x["overall_completion"])
    for d in sorted_data:
        oc = status_color(d["overall_completion"])
        completion_fig.add_trace(go.Bar(
            y=[d["project_name"]], x=[d["overall_completion"]],
            orientation="h", marker_color=oc, marker_line=dict(width=0),
            text=f"  {d['overall_completion']:.0f}%", textposition="outside",
            textfont=dict(size=12, family="Inter", weight=700, color=oc),
            showlegend=False,
            hovertemplate=f"<b>{d['project_name']}</b><br>Completion: {d['overall_completion']:.1f}%<extra></extra>",
        ))
    completion_fig.add_vline(x=75, line=dict(color=THEME["success"], width=1, dash="dot"),
                             annotation_text="Target 75%", annotation_position="top",
                             annotation_font=dict(size=9, color=THEME["success"]))
    completion_fig.update_layout(
        height=max(200, len(all_data) * 55 + 60),
        margin=dict(t=30, b=25, l=10, r=60),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"}, xaxis=dict(range=[0, 110], gridcolor="rgba(0,0,0,0.04)", ticksuffix="%"),
        yaxis=dict(tickfont={"size": 12}),
    )

    # Chart 2: SPI
    spi_fig = go.Figure()
    spi_vals = [d.get("schedule_performance_index", 1) for d in all_data]
    spi_colors = [THEME["success"] if v >= 0.9 else THEME["warning"] if v >= 0.7 else THEME["danger"] for v in spi_vals]
    spi_fig.add_trace(go.Bar(
        x=names, y=spi_vals, marker_color=spi_colors, marker_line=dict(width=0),
        text=[f"{v:.2f}" for v in spi_vals], textposition="outside",
        textfont=dict(size=11, family="Inter", weight=700),
    ))
    spi_fig.add_hline(y=1.0, line=dict(color=THEME["success"], width=1.5, dash="dash"),
                      annotation_text="On Schedule", annotation_position="top right",
                      annotation_font=dict(size=9, color=THEME["success"]))
    spi_fig.update_layout(
        height=260, margin=dict(t=30, b=35, l=45, r=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"}, yaxis=dict(gridcolor="rgba(0,0,0,0.04)", title="SPI"),
    )

    # Chart 3: Radar
    categories = ["Budget Util", "Pkg Completion", "Delivery Rate", "Overall", "Pipeline Closure"]
    radar_fig = go.Figure()
    for i, d in enumerate(all_data):
        vals = [
            min(100, d.get("budget_utilization_pct", 0)),
            d.get("pkg_completion_pct", 0),
            d.get("po_delivery_rate", 0),
            d.get("overall_completion", 0),
            d.get("pipeline_closure_rate", 0),
        ]
        vals_c = vals + [vals[0]]
        cats_c = categories + [categories[0]]
        radar_fig.add_trace(go.Scatterpolar(
            r=vals_c, theta=cats_c, name=names[i],
            fill="toself", fillcolor=hex_to_rgba(colors[i], 0.1),
            line=dict(color=colors[i], width=2.5),
        ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont={"size": 9})),
        height=320, margin=dict(t=40, b=25, l=55, r=55),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center", font={"size": 11}),
        font={"family": "Inter"},
    )

    return html.Div([
        section_title("Project Progress Analysis"),
        html.Div([
            chart_card("Procurement Completion", completion_fig),
            chart_card("Schedule Performance Index", spi_fig),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"}),
        html.Div([chart_card("Multi-Dimensional Performance Radar", radar_fig, "100%")]),
    ], style={"padding": "0 20px 16px 20px"})
