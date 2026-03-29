import plotly.graph_objects as go
from dash import html
from config import THEME, PROJECT_COLORS
from data.utils import fmt_num
from components.shared import section_title, chart_card


def make_budget_analysis(all_data):
    names = [d["project_name"] for d in all_data]
    colors = [PROJECT_COLORS[i % len(PROJECT_COLORS)]["main"] for i in range(len(all_data))]

    # Budget comparison
    budget_compare = go.Figure()
    for i, d in enumerate(all_data):
        cur = d.get("currency", "")
        budget_compare.add_trace(go.Bar(
            x=["Proposed", "Client/Effective", "Committed", "Remaining"],
            y=[d["proposed_budget"], d["effective_budget"], d["committed_spend"], d["budget_uncommitted"]],
            name=names[i], marker_color=colors[i],
            text=[fmt_num(v, cur) for v in [d["proposed_budget"], d["effective_budget"], d["committed_spend"], d["budget_uncommitted"]]],
            textposition="outside", textfont={"size": 9},
        ))
    budget_compare.update_layout(
        barmode="group", height=280, margin=dict(t=25, b=40, l=50, r=15),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center", font={"size": 11}),
        yaxis=dict(gridcolor="rgba(0,0,0,0.04)"),
    )

    # Utilization
    util_fig = go.Figure()
    for i, d in enumerate(all_data):
        util = d.get("budget_utilization_pct", 0)
        uc = THEME["danger"] if util > 95 else THEME["warning"] if util > 80 else THEME["success"]
        util_fig.add_trace(go.Bar(
            x=[names[i]], y=[util], marker_color=uc, showlegend=False,
            text=f"{util:.0f}%", textposition="outside",
            textfont=dict(size=12, weight=700),
        ))
    util_fig.add_hline(y=100, line=dict(color=THEME["danger"], width=1.5, dash="dash"), annotation_text="100%")
    util_fig.update_layout(
        height=260, margin=dict(t=30, b=35, l=45, r=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
        yaxis=dict(range=[0, max(120, max(d["budget_utilization_pct"] for d in all_data) + 20)], gridcolor="rgba(0,0,0,0.04)", ticksuffix="%"),
    )

    # Variance
    variance_fig = go.Figure()
    sorted_var = sorted(all_data, key=lambda x: x["budget_variance_pct"])
    for d in sorted_var:
        color = THEME["success"] if d["budget_variance_pct"] >= 0 else THEME["danger"]
        variance_fig.add_trace(go.Bar(
            y=[d["project_name"]], x=[d["budget_variance_pct"]],
            orientation="h", marker_color=color, showlegend=False,
            text=f"  {d['budget_variance_pct']:+.1f}%", textposition="outside",
            textfont=dict(size=11, weight=700, color=color),
        ))
    variance_fig.add_vline(x=0, line=dict(color=THEME["text_muted"], width=1))
    variance_fig.update_layout(
        height=max(180, len(all_data) * 50 + 50),
        margin=dict(t=25, b=25, l=10, r=70),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
        xaxis=dict(gridcolor="rgba(0,0,0,0.04)", ticksuffix="%", title="Budget Variance %"),
    )

    return html.Div([
        section_title("Budget Analysis"),
        html.Div([
            chart_card("Budget Comparison", budget_compare),
            chart_card("Budget Utilization %", util_fig),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"}),
        html.Div([chart_card("Budget Variance (Savings ← → Overrun)", variance_fig, "100%")]),
    ], style={"padding": "0 20px 16px 20px"})
