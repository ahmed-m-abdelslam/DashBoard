import plotly.graph_objects as go
from dash import html
from config import THEME
from components.shared import section_title, chart_card


def make_delivery_analysis(all_data):
    names = [d["project_name"] for d in all_data]

    po_fig = go.Figure()
    po_fig.add_trace(go.Bar(x=names, y=[d["total_pos"] for d in all_data], name="Total POs", marker_color=THEME["info"]))
    po_fig.add_trace(go.Bar(x=names, y=[d["delivered_pos"] for d in all_data], name="Delivered", marker_color=THEME["success"]))
    po_fig.add_trace(go.Bar(x=names, y=[d["outstanding_pos"] for d in all_data], name="Outstanding", marker_color=THEME["danger"]))
    po_fig.update_layout(
        barmode="group", height=280, margin=dict(t=25, b=35, l=45, r=15),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center", font={"size": 11}),
        yaxis=dict(gridcolor="rgba(0,0,0,0.04)"),
    )

    delivery_rate_fig = go.Figure()
    for i, d in enumerate(all_data):
        dr = d["po_delivery_rate"]
        dc = THEME["success"] if dr >= 70 else THEME["warning"] if dr >= 40 else THEME["danger"]
        delivery_rate_fig.add_trace(go.Bar(x=[names[i]], y=[dr], marker_color=dc, showlegend=False,
            text=f"{dr:.0f}%", textposition="outside", textfont=dict(size=12, weight=700)))
    delivery_rate_fig.add_trace(go.Scatter(
        x=names, y=[d["delivery_gap"] for d in all_data], mode="lines+markers+text",
        name="Delivery Gap", line=dict(color=THEME["orange"], width=2.5, dash="dot"),
        marker=dict(size=8, color=THEME["orange"]),
        text=[f"{d['delivery_gap']:.0f}pp" for d in all_data],
        textposition="top center", textfont=dict(size=10, color=THEME["orange"]), yaxis="y2",
    ))
    delivery_rate_fig.update_layout(
        height=280, margin=dict(t=30, b=35, l=45, r=45),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
        yaxis=dict(title="Delivery Rate %", gridcolor="rgba(0,0,0,0.04)", ticksuffix="%"),
        yaxis2=dict(title="Delivery Gap (pp)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center", font={"size": 11}),
    )

    return html.Div([
        section_title("Purchase Order & Delivery Tracking"),
        html.Div([
            chart_card("PO Status Overview", po_fig),
            chart_card("Delivery Rate & Procurement Gap", delivery_rate_fig),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap"}),
    ], style={"padding": "0 20px 16px 20px"})
