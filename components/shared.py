from dash import html, dcc
from config import THEME, FONT
from data.utils import hex_to_rgba


def glass_card(extra=None):
    base = {
        "backgroundColor": "rgba(255,255,255,0.95)",
        "backdropFilter": "blur(20px)",
        "WebkitBackdropFilter": "blur(20px)",
        "borderRadius": "16px",
        "border": "1px solid rgba(226,232,240,0.6)",
        "boxShadow": "0 1px 3px rgba(0,0,0,0.03), 0 4px 20px rgba(0,0,0,0.04)",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
    }
    if extra:
        base.update(extra)
    return base


def section_title(text):
    return html.H2(text, className="section-title", style={
        "fontSize": FONT["lg"], "color": THEME["text"], "fontWeight": "800",
        "margin": "0 0 20px 0", "paddingBottom": "12px",
        "borderBottom": f"2px solid {THEME['border']}",
        "letterSpacing": "-0.3px",
    })


def chart_card(title, figure, min_width="340px"):
    return html.Div([
        html.H3(title, style={
            "fontSize": FONT["md"], "color": THEME["text"],
            "fontWeight": "700", "margin": "0 0 8px 0",
            "letterSpacing": "-0.2px",
        }),
        dcc.Graph(figure=figure, config={"displayModeBar": False}),
    ], className="chart-card", style=glass_card({
        "padding": "20px 22px",
        "flex": "1",
        "minWidth": min_width,
    }))


def make_progress_bar(label, value, max_val, color, show_fraction=True):
    pct = min(100, (value / max_val * 100) if max_val > 0 else 0)
    right_text = f"{int(value)}/{int(max_val)}" if show_fraction else f"{pct:.0f}%"

    # Gradient for progress bar
    lighter = hex_to_rgba(color, 0.7)

    return html.Div([
        html.Div([
            html.Span(label, style={
                "fontSize": FONT["sm"], "color": THEME["text"], "fontWeight": "600",
            }),
            html.Span(right_text, style={
                "fontSize": FONT["sm"], "color": color, "fontWeight": "700",
            }),
        ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "6px"}),
        html.Div([
            html.Div(style={
                "width": f"{pct}%",
                "height": "100%",
                "background": f"linear-gradient(90deg, {color}, {lighter})",
                "borderRadius": "6px",
                "transition": "width 1s cubic-bezier(0.4, 0, 0.2, 1)",
                "boxShadow": f"0 0 8px {hex_to_rgba(color, 0.3)}",
            })
        ], style={
            "width": "100%", "height": "8px",
            "backgroundColor": hex_to_rgba(color, 0.08),
            "borderRadius": "6px", "overflow": "hidden",
        }),
    ], style={"marginBottom": "14px"})


def kpi_chip(label, value, icon, color):
    return html.Div([
        html.Div([
            html.Span(icon, style={"fontSize": "16px"}),
        ], style={
            "width": "32px", "height": "32px", "borderRadius": "8px",
            "backgroundColor": hex_to_rgba(color, 0.1),
            "display": "flex", "alignItems": "center", "justifyContent": "center",
        }),
        html.Div([
            html.P(label, style={
                "fontSize": "9px", "color": THEME["text_muted"], "margin": "0",
                "textTransform": "uppercase", "letterSpacing": "0.8px", "fontWeight": "600",
            }),
            html.P(value, style={
                "fontSize": FONT["md"], "color": THEME["text"],
                "margin": "2px 0 0 0", "fontWeight": "800",
            }),
        ]),
    ], className="kpi-chip", style={
        "display": "flex", "alignItems": "center", "gap": "10px",
        "backgroundColor": hex_to_rgba(color, 0.04),
        "padding": "10px 14px", "borderRadius": "12px",
        "border": f"1px solid {hex_to_rgba(color, 0.08)}",
        "flex": "1", "minWidth": "120px",
        "transition": "all 0.2s ease",
    })


def status_badge(text, active):
    color = THEME["success"] if active else THEME["text_muted"]
    icon = "✓" if active else "○"
    return html.Span(f"{icon} {text}", className="status-badge", style={
        "fontSize": "10px", "fontWeight": "700", "color": color,
        "backgroundColor": hex_to_rgba(color, 0.08),
        "padding": "4px 10px", "borderRadius": "20px",
        "border": f"1px solid {hex_to_rgba(color, 0.15)}",
        "transition": "all 0.2s ease",
    })


def concern_badge(category):
    cat_colors = {
        "Supplier": THEME["purple"], "Timeline": THEME["danger"],
        "Cost": THEME["orange"], "Quality": THEME["pink"],
        "Approval": THEME["warning"], "Logistics": THEME["cyan"],
    }
    color = cat_colors.get(category, THEME["text_muted"])
    return html.Span(category, className="status-badge", style={
        "fontSize": "10px", "fontWeight": "700", "color": color,
        "backgroundColor": hex_to_rgba(color, 0.08),
        "padding": "3px 10px", "borderRadius": "20px",
        "border": f"1px solid {hex_to_rgba(color, 0.12)}",
    })
