from dash import html
from config import THEME, FONT


def make_topbar():
    return html.Div([
        html.Div([
            html.Div(style={
                "width": "38px", "height": "38px", "borderRadius": "10px",
                "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                "overflow": "hidden",
                "boxShadow": "0 2px 8px rgba(99,102,241,0.3)",
            }, children=[
                html.Img(src="/assets/luxurylogo.jpg", style={
                    "height": "38px", "width": "38px", "objectFit": "cover",
                })
            ]),
            html.Div([
                html.H1("Luxury Hospitality", style={
                    "margin": "0", "color": "#fff", "fontSize": FONT["lg"],
                    "fontWeight": "800", "letterSpacing": "-0.3px",
                }),
                html.P("Procurement Analytics & Risk Intelligence", style={
                    "color": "rgba(255,255,255,0.35)", "fontSize": "10px",
                    "margin": "2px 0 0 0", "letterSpacing": "0.5px",
                    "fontWeight": "500",
                }),
            ]),
        ], style={"display": "flex", "alignItems": "center", "gap": "12px", "flex": "1"}),

        html.Div([
            # Live indicator
            html.Div([
                html.Div(style={
                    "width": "6px", "height": "6px", "borderRadius": "50%",
                    "backgroundColor": "#10b981",
                    "boxShadow": "0 0 6px rgba(16,185,129,0.5)",
                    "animation": "pulse-glow 2s ease-in-out infinite",
                }),
                html.Span("Live", style={
                    "fontSize": "10px", "color": "#10b981",
                    "fontWeight": "700", "letterSpacing": "0.5px",
                }),
            ], style={
                "display": "flex", "alignItems": "center", "gap": "5px",
                "backgroundColor": "rgba(16,185,129,0.1)",
                "padding": "5px 12px", "borderRadius": "20px",
                "border": "1px solid rgba(16,185,129,0.2)",
            }),

            html.Button(
                [html.Span("⛶", style={"fontSize": "14px"}), html.Span("Fullscreen")],
                id="btn-fullscreen", n_clicks=0,
                style={
                    "backgroundColor": "rgba(99,102,241,0.12)", "color": "#a5b4fc",
                    "border": "1px solid rgba(99,102,241,0.25)",
                    "padding": "7px 16px", "borderRadius": "10px", "cursor": "pointer",
                    "fontSize": FONT["sm"], "fontWeight": "600",
                    "display": "flex", "alignItems": "center", "gap": "6px",
                    "transition": "all 0.2s ease",
                },
            ),
            html.Button(
                [html.Span("✕", style={"fontSize": "12px"}), html.Span("Exit")],
                id="btn-exit-fullscreen", n_clicks=0,
                style={
                    "backgroundColor": "rgba(239,68,68,0.12)", "color": "#fca5a5",
                    "border": "1px solid rgba(239,68,68,0.25)",
                    "padding": "7px 16px", "borderRadius": "10px", "cursor": "pointer",
                    "fontSize": FONT["sm"], "fontWeight": "600",
                    "display": "none", "alignItems": "center", "gap": "6px",
                    "transition": "all 0.2s ease",
                },
            ),
            html.A("← New File", href="/", style={
                "backgroundColor": "rgba(255,255,255,0.06)", "color": "#e2e8f0",
                "border": "1px solid rgba(255,255,255,0.08)",
                "padding": "7px 16px", "borderRadius": "10px",
                "fontSize": FONT["sm"], "fontWeight": "600", "textDecoration": "none",
                "transition": "all 0.2s ease",
            }),
        ], style={"display": "flex", "alignItems": "center", "gap": "8px"}),
    ], id="top-bar", className="top-bar", style={
        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
        "background": f"linear-gradient(135deg, {THEME['dark']} 0%, {THEME['dark2']} 60%, rgba(99,102,241,0.08) 100%)",
        "padding": "10px 24px", "marginBottom": "18px",
        "boxShadow": "0 4px 20px rgba(0,0,0,0.15)",
        "position": "sticky", "top": "0", "zIndex": "1000",
        "backdropFilter": "blur(20px)",
    })
