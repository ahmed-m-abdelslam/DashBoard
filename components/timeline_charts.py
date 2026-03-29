import plotly.graph_objects as go
import pandas as pd
from dash import html
from config import THEME, PROJECT_COLORS
from data.utils import urgency_color
from components.shared import section_title, chart_card


def make_timeline_analysis(all_data):
    today = pd.Timestamp.now()
    fig = go.Figure()

    for i, d in enumerate(all_data):
        pc = PROJECT_COLORS[i % len(PROJECT_COLORS)]
        name = d["project_name"]
        parsed = d.get("opening_date_parsed")
        opening_str = d.get("opening_date", "TBD")
        uc = urgency_color(d.get("urgency_category", "TBD"))

        if opening_str == "Opened":
            fig.add_trace(go.Scatter(
                x=[today], y=[name], mode="markers+text",
                marker=dict(size=16, color=THEME["success"], symbol="star", line=dict(width=2, color="#fff")),
                text=["  OPENED"], textposition="middle right",
                textfont=dict(size=11, color=THEME["success"], weight=700), showlegend=False,
            ))
        elif parsed is not None:
            days_left = (parsed - today).days
            fig.add_trace(go.Scatter(
                x=[today, parsed], y=[name, name], mode="lines",
                line=dict(color=pc["main"], width=8), showlegend=False, hoverinfo="skip",
            ))
            label = f"  {days_left}d" if days_left > 0 else f"  {abs(days_left)}d overdue"
            fig.add_trace(go.Scatter(
                x=[parsed], y=[name], mode="markers+text",
                marker=dict(size=14, color=uc, symbol="diamond", line=dict(width=2, color="#fff")),
                text=[label], textposition="middle right",
                textfont=dict(size=11, color=uc, weight=700), showlegend=False,
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[today], y=[name], mode="markers+text",
                marker=dict(size=12, color=THEME["text_muted"], symbol="circle"),
                text=["  TBD"], textposition="middle right",
                textfont=dict(size=11, color=THEME["text_muted"]), showlegend=False,
            ))

    fig.add_vline(x=today.timestamp() * 1000, line=dict(color=THEME["danger"], width=1.5, dash="dot"), annotation_text="Today")
    fig.update_layout(
        height=max(180, len(all_data) * 60 + 50), margin=dict(t=35, b=30, l=15, r=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
    )

    # Urgency donut
    urgency_counts = {}
    for d in all_data:
        cat = d.get("urgency_category", "TBD")
        urgency_counts[cat] = urgency_counts.get(cat, 0) + 1

    urg_fig = go.Figure(go.Pie(
        labels=list(urgency_counts.keys()), values=list(urgency_counts.values()),
        marker=dict(colors=[urgency_color(k) for k in urgency_counts.keys()]),
        hole=0.5, textinfo="label+value", textfont=dict(size=12),
    ))
    urg_fig.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", showlegend=False, font={"family": "Inter"})

    return html.Div([
        section_title("Timeline Analysis"),
        html.Div([
            chart_card("Project Opening Timeline", fig, "55%"),
            chart_card("Urgency Distribution", urg_fig, "280px"),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap"}),
    ], style={"padding": "0 20px 16px 20px"})
