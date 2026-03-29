from dash import html, dcc
from config import THEME, FONT
from components.shared import glass_card


def make_upload_section():
    return html.Div(id="upload-section", children=[
        html.Div(style={"height": "10vh"}),
        html.Div([
            # Decorative top gradient line
            html.Div(style={
                "height": "4px",
                "background": "linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4)",
                "borderRadius": "16px 16px 0 0",
                "marginBottom": "0",
            }),
            html.Div([
                # Logo with glow effect
                html.Div(style={
                    "width": "76px", "height": "76px", "borderRadius": "20px",
                    "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                    "display": "flex", "alignItems": "center", "justifyContent": "center",
                    "margin": "0 auto 20px auto", "overflow": "hidden",
                    "boxShadow": "0 8px 32px rgba(99,102,241,0.35), 0 0 0 4px rgba(99,102,241,0.1)",
                    "animation": "pulse-glow 3s ease-in-out infinite",
                }, children=[
                    html.Img(src="/assets/luxurylogo.jpg", style={
                        "height": "76px", "width": "76px", "objectFit": "cover",
                    })
                ]),

                # Title
                html.H1("Procurement Dashboard", style={
                    "margin": "0 0 4px 0", "color": THEME["text"],
                    "fontSize": "30px", "fontWeight": "900", "letterSpacing": "-0.8px",
                    "lineHeight": "1.2",
                }),
                html.P("Luxury Hospitality Intelligence", style={
                    "color": THEME["indigo"], "fontSize": FONT["sm"],
                    "margin": "0 0 4px 0", "fontWeight": "700",
                    "letterSpacing": "2px", "textTransform": "uppercase",
                }),
                html.P("Upload procurement data for AI-powered analytics", style={
                    "color": THEME["text_muted"], "fontSize": FONT["md"],
                    "margin": "0 0 32px 0", "fontWeight": "400",
                }),

                # Upload area
                dcc.Upload(
                    id="upload-data",
                    children=html.Div([
                        # Icon container
                        html.Div(style={
                            "width": "56px", "height": "56px", "borderRadius": "16px",
                            "background": "linear-gradient(135deg, #eef2ff, #e0e7ff)",
                            "display": "flex", "alignItems": "center", "justifyContent": "center",
                            "margin": "0 auto 14px auto",
                            "boxShadow": "0 4px 12px rgba(99,102,241,0.1)",
                        }, children=[
                            html.Span("📊", style={"fontSize": "26px"})
                        ]),
                        html.P("Drag & Drop or Click to Upload", style={
                            "fontWeight": "700", "color": "#6366f1",
                            "fontSize": FONT["lg"], "margin": "0 0 6px 0",
                        }),
                        html.P("Supports .xlsx  ·  .xlsm  ·  .xls  ·  .csv", style={
                            "color": THEME["text_muted"], "fontSize": FONT["sm"],
                            "margin": "0 0 4px 0",
                        }),
                        html.P("Max file size: 10MB", style={
                            "color": THEME["text_muted"], "fontSize": FONT["xs"],
                            "margin": "0", "opacity": "0.6",
                        }),
                    ]),
                    className="upload-area",
                    style={
                        "width": "100%", "padding": "40px 20px",
                        "borderWidth": "2px", "borderStyle": "dashed",
                        "borderColor": "#c7d2fe", "borderRadius": "16px",
                        "textAlign": "center",
                        "backgroundColor": "rgba(238,242,255,0.4)",
                        "cursor": "pointer",
                        "transition": "all 0.3s ease",
                    },
                    multiple=False,
                ),

                # Features hint
                html.Div([
                    html.Div([
                        html.Span("🤖", style={"fontSize": "14px"}),
                        html.Span("AI Analysis", style={"fontSize": FONT["xs"], "color": THEME["text_light"], "fontWeight": "600"}),
                    ], style={"display": "flex", "alignItems": "center", "gap": "5px"}),
                    html.Span("·", style={"color": THEME["border"]}),
                    html.Div([
                        html.Span("📈", style={"fontSize": "14px"}),
                        html.Span("Risk Scoring", style={"fontSize": FONT["xs"], "color": THEME["text_light"], "fontWeight": "600"}),
                    ], style={"display": "flex", "alignItems": "center", "gap": "5px"}),
                    html.Span("·", style={"color": THEME["border"]}),
                    html.Div([
                        html.Span("📊", style={"fontSize": "14px"}),
                        html.Span("Visual Reports", style={"fontSize": FONT["xs"], "color": THEME["text_light"], "fontWeight": "600"}),
                    ], style={"display": "flex", "alignItems": "center", "gap": "5px"}),
                ], style={
                    "display": "flex", "justifyContent": "center",
                    "gap": "12px", "marginTop": "20px",
                    "padding": "12px", "backgroundColor": "rgba(248,250,252,0.6)",
                    "borderRadius": "10px",
                }),

                html.Div(id="upload-error", style={"marginTop": "14px"}),
            ], style={"padding": "36px 52px 44px 52px"}),
        ], style=glass_card({
            "maxWidth": "500px", "margin": "0 auto",
            "textAlign": "center", "overflow": "hidden",
            "padding": "0",
            "boxShadow": "0 4px 40px rgba(0,0,0,0.06), 0 0 0 1px rgba(226,232,240,0.5)",
        })),
    ])
