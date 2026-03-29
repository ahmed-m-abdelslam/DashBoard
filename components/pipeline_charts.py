import plotly.graph_objects as go
from dash import html
from config import THEME
from components.shared import section_title, chart_card


def make_procurement_pipeline(all_data):
    names = [d["project_name"] for d in all_data]

    pkg_fig = go.Figure()
    pkg_fig.add_trace(go.Bar(x=names, y=[d["packages_completed"] for d in all_data], name="Completed", marker_color=THEME["success"],
        text=[f"{int(d['packages_completed'])}" for d in all_data], textposition="inside", textfont={"size": 11, "color": "#fff"}))
    pkg_fig.add_trace(go.Bar(x=names, y=[d["packages_in_progress"] for d in all_data], name="In Progress", marker_color=THEME["warning"],
        text=[f"{int(d['packages_in_progress'])}" if d["packages_in_progress"] > 0 else "" for d in all_data], textposition="inside", textfont={"size": 11, "color": "#fff"}))
    pkg_fig.add_trace(go.Bar(x=names, y=[d["packages_to_start"] for d in all_data], name="Not Started", marker_color="#e2e8f0",
        text=[f"{int(d['packages_to_start'])}" if d["packages_to_start"] > 0 else "" for d in all_data], textposition="inside", textfont={"size": 11, "color": "#94a3b8"}))
    pkg_fig.update_layout(
        barmode="stack", height=280, margin=dict(t=25, b=35, l=40, r=15),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center", font={"size": 11}),
        yaxis=dict(gridcolor="rgba(0,0,0,0.04)", title="Packages"),
    )

    pipeline_fig = go.Figure()
    pipeline_fig.add_trace(go.Bar(x=names, y=[d["pipeline_initiation_rate"] for d in all_data], name="Initiation Rate", marker_color=THEME["info"],
        text=[f"{d['pipeline_initiation_rate']:.0f}%" for d in all_data], textposition="outside", textfont={"size": 10}))
    pipeline_fig.add_trace(go.Bar(x=names, y=[d["pipeline_closure_rate"] for d in all_data], name="Closure Rate", marker_color=THEME["purple"],
        text=[f"{d['pipeline_closure_rate']:.0f}%" for d in all_data], textposition="outside", textfont={"size": 10}))
    pipeline_fig.update_layout(
        barmode="group", height=260, margin=dict(t=25, b=35, l=45, r=15),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center", font={"size": 11}),
        yaxis=dict(gridcolor="rgba(0,0,0,0.04)", ticksuffix="%", range=[0, 115]),
    )

    return html.Div([
        section_title("Procurement Pipeline"),
        html.Div([
            chart_card("Package Status Breakdown", pkg_fig),
            chart_card("Pipeline Efficiency Rates", pipeline_fig),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap"}),
    ], style={"padding": "0 20px 16px 20px"})
