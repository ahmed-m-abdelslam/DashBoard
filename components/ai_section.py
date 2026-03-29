from dash import html
from config import THEME, FONT
from components.shared import glass_card


def make_ai_portfolio_section(ai_text):
    return html.Div([
        html.Div([
            # Animated top border
            html.Div(style={
                "height": "3px",
                "background": "linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4, #6366f1)",
                "backgroundSize": "300% 100%",
                "animation": "gradient-shift 4s linear infinite",
                "borderRadius": "16px 16px 0 0",
            }),
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("🤖", style={"fontSize": "20px"}),
                    ], style={
                        "width": "36px", "height": "36px", "borderRadius": "10px",
                        "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                        "display": "flex", "alignItems": "center", "justifyContent": "center",
                        "boxShadow": "0 2px 8px rgba(99,102,241,0.2)",
                    }),
                    html.Div([
                        html.Span("AI Portfolio Analysis", style={
                            "fontSize": FONT["md"], "fontWeight": "800",
                            "color": THEME["text"], "letterSpacing": "-0.2px",
                        }),
                        html.Span("Powered by LLaMA 3.3", style={
                            "fontSize": "9px", "color": THEME["text_muted"],
                            "marginLeft": "8px", "fontWeight": "600",
                            "backgroundColor": "rgba(99,102,241,0.06)",
                            "padding": "2px 8px", "borderRadius": "8px",
                        }),
                    ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap"}),
                ], style={"display": "flex", "alignItems": "center", "gap": "10px", "marginBottom": "16px"}),
                html.Div(ai_text, style={
                    "fontSize": FONT["sm"], "lineHeight": "1.8",
                    "color": THEME["dark3"], "whiteSpace": "pre-line",
                }),
            ], style={"padding": "22px 26px"}),
        ], className="ai-section", style=glass_card({
            "overflow": "hidden", "padding": "0",
            "border": "1px solid rgba(99,102,241,0.12)",
        })),
    ], style={"padding": "0 20px 18px 20px"})
