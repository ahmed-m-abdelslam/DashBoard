from datetime import datetime
from dash import html
from config import THEME, FONT, PROJECT_COLORS
from data.utils import hex_to_rgba, fmt_num, status_color, urgency_color


def _kpi_card(icon, value, label, sublabel="", trend_color=None):
    return html.Div([
        html.Div([
            html.Div([
                html.Span(icon, style={"fontSize": "22px"}),
            ], style={
                "width": "40px", "height": "40px", "borderRadius": "10px",
                "backgroundColor": "rgba(255,255,255,0.08)",
                "display": "flex", "alignItems": "center", "justifyContent": "center",
                "flexShrink": "0",
            }),
            html.Div([
                html.P(value, style={
                    "fontSize": FONT["xl"], "fontWeight": "900",
                    "color": "#fff", "margin": "0", "lineHeight": "1.1",
                    "letterSpacing": "-0.3px",
                }),
                html.P(label, style={
                    "fontSize": "9px", "color": "rgba(255,255,255,0.45)",
                    "margin": "4px 0 0 0", "textTransform": "uppercase",
                    "letterSpacing": "1.2px", "fontWeight": "700",
                }),
                html.P(sublabel, style={
                    "fontSize": "10px", "margin": "3px 0 0 0", "fontWeight": "600",
                    "color": trend_color or "rgba(255,255,255,0.3)",
                }) if sublabel else html.Div(),
            ]),
        ], style={"display": "flex", "alignItems": "center", "gap": "12px"}),
    ], className="kpi-card", style={
        "backgroundColor": "rgba(255,255,255,0.05)",
        "padding": "16px 20px", "borderRadius": "14px",
        "border": "1px solid rgba(255,255,255,0.06)",
        "flex": "1", "minWidth": "165px",
        "transition": "all 0.3s ease",
        "position": "relative", "overflow": "hidden",
    })


def _project_mini(data, index):
    pc = PROJECT_COLORS[index % len(PROJECT_COLORS)]
    oc = status_color(data["overall_completion"])
    uc = urgency_color(data.get("urgency_category", "TBD"))
    return html.Div([
        html.Div(style={
            "width": "8px", "height": "8px", "borderRadius": "50%",
            "backgroundColor": pc["main"], "flexShrink": "0",
            "boxShadow": f"0 0 6px {hex_to_rgba(pc['main'], 0.4)}",
        }),
        html.Div([
            html.Span(data["project_name"], style={
                "fontSize": FONT["sm"], "fontWeight": "600", "color": "#e2e8f0",
                "lineHeight": "1.2",
            }),
            html.Div([
                html.Span(f"{data['overall_completion']:.0f}%", style={
                    "fontSize": "10px", "fontWeight": "800", "color": oc,
                    "backgroundColor": hex_to_rgba(oc, 0.15),
                    "padding": "2px 8px", "borderRadius": "6px",
                }),
                html.Span(data.get("urgency_category", "TBD"), style={
                    "fontSize": "9px", "fontWeight": "700", "color": uc,
                    "backgroundColor": hex_to_rgba(uc, 0.15),
                    "padding": "2px 8px", "borderRadius": "6px",
                }),
            ], style={"display": "flex", "gap": "4px", "marginTop": "4px"}),
        ]),
    ], className="mini-card", style={
        "display": "flex", "alignItems": "center", "gap": "10px",
        "backgroundColor": "rgba(255,255,255,0.04)",
        "padding": "10px 16px", "borderRadius": "10px",
        "border": "1px solid rgba(255,255,255,0.05)",
        "transition": "all 0.3s ease",
    })


def make_portfolio_header(all_data):
    n = len(all_data)
    active = sum(1 for d in all_data if d.get("overall_completion", 0) > 0)
    at_risk = sum(1 for d in all_data if d.get("risk_score", 0) >= 50)

    total_budget = sum(d.get("effective_budget", 0) for d in all_data)
    total_committed = sum(d.get("committed_spend", 0) for d in all_data)
    total_packages = sum(d.get("total_packages", 0) for d in all_data)
    total_pkg_done = sum(d.get("packages_completed", 0) for d in all_data)
    total_pos = sum(d.get("total_pos", 0) for d in all_data)
    total_delivered = sum(d.get("delivered_pos", 0) for d in all_data)

    avg_completion = sum(d.get("overall_completion", 0) for d in all_data) / n if n > 0 else 0
    weighted_completion = sum(d["overall_completion"] * d["effective_budget"] for d in all_data) / total_budget if total_budget > 0 else avg_completion
    delivery_rate = (total_delivered / total_pos * 100) if total_pos > 0 else 0
    budget_util = (total_committed / total_budget * 100) if total_budget > 0 else 0

    kpis = html.Div([
        _kpi_card("📊", f"{avg_completion:.0f}%", "Avg Completion", f"Weighted: {weighted_completion:.0f}%", "#a5b4fc"),
        _kpi_card("💰", fmt_num(total_budget), "Total Budget", f"Util: {budget_util:.0f}%", "#fca5a5" if budget_util > 90 else "#86efac"),
        _kpi_card("📦", f"{int(total_pkg_done)}/{int(total_packages)}", "Packages", f"{total_pkg_done/total_packages*100:.0f}% Done" if total_packages > 0 else ""),
        _kpi_card("🚚", f"{int(total_delivered)}/{int(total_pos)}", "Deliveries", f"Rate: {delivery_rate:.0f}%", "#fca5a5" if delivery_rate < 50 else "#86efac"),
        _kpi_card("⚡", str(active), "Active", f"{at_risk} at risk", "#fca5a5" if at_risk > 0 else "#86efac"),
    ], style={"display": "flex", "gap": "12px", "flexWrap": "wrap"})

    minis = html.Div([_project_mini(d, i) for i, d in enumerate(all_data)], style={
        "display": "flex", "gap": "8px", "flexWrap": "wrap", "justifyContent": "flex-end", "flex": "1",
    })

    return html.Div([
        html.Div([
            html.Div([
                html.H2("Portfolio Overview", style={
                    "margin": "0", "color": "#fff", "fontSize": FONT["xxl"],
                    "fontWeight": "900", "letterSpacing": "-0.7px",
                }),
                html.P(
                    f"{n} Projects  ·  {active} Active  ·  {at_risk} At Risk  ·  {datetime.now().strftime('%d %b %Y')}",
                    style={
                        "margin": "6px 0 0 0", "color": "rgba(255,255,255,0.35)",
                        "fontSize": FONT["sm"], "fontWeight": "500", "letterSpacing": "0.2px",
                    },
                ),
            ]),
            minis,
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "alignItems": "center", "gap": "24px",
            "flexWrap": "wrap", "marginBottom": "18px",
        }),
        kpis,
    ], className="portfolio-header", style={
        "background": f"linear-gradient(135deg, {THEME['dark']} 0%, {THEME['dark2']} 40%, rgba(99,102,241,0.12) 100%)",
        "padding": "28px 32px", "borderRadius": "18px",
        "margin": "0 20px 20px 20px",
        "boxShadow": "0 4px 30px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.05)",
        "position": "relative", "overflow": "hidden",
    })
