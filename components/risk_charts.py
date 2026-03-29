import plotly.graph_objects as go
from dash import html
from config import THEME, PROJECT_COLORS
from data.utils import hex_to_rgba, risk_color, risk_label
from components.shared import section_title, chart_card


def make_risk_analysis(all_data):
    names = [d["project_name"] for d in all_data]

    # Risk scores
    risk_fig = go.Figure()
    sorted_risk = sorted(all_data, key=lambda x: x["risk_score"], reverse=True)
    for d in sorted_risk:
        rc = risk_color(d["risk_score"])
        risk_fig.add_trace(go.Bar(
            y=[d["project_name"]], x=[d["risk_score"]], orientation="h",
            marker_color=rc, showlegend=False,
            text=f"  {d['risk_score']}", textposition="outside",
            textfont=dict(size=12, weight=700, color=rc),
        ))
    risk_fig.add_vline(x=60, line=dict(color=THEME["danger"], width=1, dash="dash"), annotation_text="High Risk")
    risk_fig.add_vline(x=30, line=dict(color=THEME["warning"], width=1, dash="dot"), annotation_text="Medium")
    risk_fig.update_layout(
        height=max(200, len(all_data) * 50 + 50),
        margin=dict(t=25, b=25, l=10, r=60),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"}, xaxis=dict(range=[0, 110], gridcolor="rgba(0,0,0,0.04)"),
    )

    # Risk scatter
    scatter_fig = go.Figure()
    for i, d in enumerate(all_data):
        dt = d.get("days_to_opening") or 400
        rc = risk_color(d["risk_score"])
        scatter_fig.add_trace(go.Scatter(
            x=[dt], y=[d["overall_completion"]], mode="markers+text",
            marker=dict(size=max(12, d["risk_score"] / 3), color=rc, line=dict(width=2, color="#fff"), opacity=0.85),
            text=[d["project_name"]], textposition="top center", textfont=dict(size=10),
            showlegend=False,
        ))
    scatter_fig.add_hline(y=50, line=dict(color=THEME["warning"], width=1, dash="dot"))
    scatter_fig.add_vline(x=90, line=dict(color=THEME["danger"], width=1, dash="dot"))
    scatter_fig.add_annotation(x=45, y=25, text="⚠ DANGER ZONE", font=dict(size=12, color=THEME["danger"]),
                               showarrow=False, bgcolor=hex_to_rgba(THEME["danger"], 0.08), borderpad=6)
    scatter_fig.update_layout(
        height=320, margin=dict(t=25, b=40, l=50, r=25),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
        xaxis=dict(title="Days to Opening", gridcolor="rgba(0,0,0,0.04)"),
        yaxis=dict(title="Completion %", gridcolor="rgba(0,0,0,0.04)", ticksuffix="%"),
    )

    # Concern categories
    all_categories = {}
    for d in all_data:
        for cat in d.get("concern_categories", []):
            all_categories[cat] = all_categories.get(cat, 0) + 1

    if all_categories:
        cats = sorted(all_categories.items(), key=lambda x: x[1], reverse=True)
        cat_fig = go.Figure(go.Bar(
            x=[c[1] for c in cats], y=[c[0] for c in cats], orientation="h",
            marker_color=THEME["orange"], text=[str(c[1]) for c in cats], textposition="outside",
        ))
        cat_fig.update_layout(
            height=max(150, len(cats) * 40 + 50), margin=dict(t=15, b=20, l=10, r=40),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
        )
    else:
        cat_fig = go.Figure()
        cat_fig.update_layout(height=150, paper_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text="No concerns categorized", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)])

    return html.Div([
        section_title("Risk Analysis"),
        html.Div([
            chart_card("Composite Risk Scores", risk_fig),
            chart_card("Risk Matrix: Completion vs Timeline", scatter_fig, "400px"),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"}),
        html.Div([chart_card("Concern Categories Distribution", cat_fig, "100%")]),
    ], style={"padding": "0 20px 16px 20px"})
