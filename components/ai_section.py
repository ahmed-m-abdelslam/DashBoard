from dash import html, dcc
from config import THEME, FONT
from components.shared import glass_card


def make_ai_portfolio_section_placeholder():
    """Shows loading state, AI loads via callback."""
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Span("🤖", style={"fontSize": "20px"}),
                ], style={
                    "width": "36px", "height": "36px", "borderRadius": "10px",
                    "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                    "display": "flex", "alignItems": "center",
                    "justifyContent": "center",
                }),
                html.Div([
                    html.Span("AI Portfolio Analysis", style={
                        "fontSize": FONT["md"], "fontWeight": "800",
                        "color": THEME["text"],
                    }),
                    html.Span("Powered by LLaMA 3.3", style={
                        "fontSize": "9px", "color": THEME["text_muted"],
                        "marginLeft": "8px", "fontWeight": "600",
                        "backgroundColor": "rgba(99,102,241,0.06)",
                        "padding": "2px 8px", "borderRadius": "8px",
                    }),
                ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap"}),
            ], style={"display": "flex", "alignItems": "center", "gap": "10px", "marginBottom": "16px"}),

            # This div gets replaced by the AI callback
            html.Div(
                id="ai-portfolio-content",
                children=[
                    dcc.Loading(
                        type="dot",
                        color="#6366f1",
                        children=html.Div([
                            html.Div([
                                html.Div(style={
                                    "height": "10px", "width": "85%",
                                    "backgroundColor": "rgba(99,102,241,0.08)",
                                    "borderRadius": "5px", "marginBottom": "8px",
                                    "animation": "shimmer 1.5s ease-in-out infinite",
                                    "background": "linear-gradient(90deg, rgba(99,102,241,0.05), rgba(99,102,241,0.12), rgba(99,102,241,0.05))",
                                    "backgroundSize": "200% 100%",
                                }),
                                html.Div(style={
                                    "height": "10px", "width": "70%",
                                    "backgroundColor": "rgba(99,102,241,0.06)",
                                    "borderRadius": "5px", "marginBottom": "8px",
                                }),
                                html.Div(style={
                                    "height": "10px", "width": "90%",
                                    "backgroundColor": "rgba(99,102,241,0.04)",
                                    "borderRadius": "5px",
                                }),
                            ]),
                            html.P("Analyzing portfolio data...", style={
                                "color": THEME["text_muted"], "fontSize": FONT["xs"],
                                "marginTop": "12px", "fontStyle": "italic",
                            }),
                        ], style={"minHeight": "80px"}),
                    ),
                ],
            ),
        ], style={"padding": "22px 26px"}),
    ], className="ai-section", style=glass_card({
        "overflow": "hidden", "padding": "0",
        "border": "1px solid rgba(99,102,241,0.12)",
    }), style2={"padding": "0 20px 18px 20px"})


# Fix: style2 doesn't exist, wrap properly
def make_ai_portfolio_section_placeholder():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Span("🤖", style={"fontSize": "20px"}),
                ], style={
                    "width": "36px", "height": "36px", "borderRadius": "10px",
                    "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                    "display": "flex", "alignItems": "center",
                    "justifyContent": "center",
                }),
                html.Div([
                    html.Span("AI Portfolio Analysis", style={
                        "fontSize": FONT["md"], "fontWeight": "800",
                        "color": THEME["text"],
                    }),
                    html.Span("Powered by LLaMA 3.3", style={
                        "fontSize": "9px", "color": THEME["text_muted"],
                        "marginLeft": "8px", "fontWeight": "600",
                        "backgroundColor": "rgba(99,102,241,0.06)",
                        "padding": "2px 8px", "borderRadius": "8px",
                    }),
                ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap"}),
            ], style={"display": "flex", "alignItems": "center", "gap": "10px", "marginBottom": "16px"}),

            html.Div(
                id="ai-portfolio-content",
                children=[
                    html.Div([
                        html.Div(style={
                            "height": "10px", "width": "85%",
                            "background": "linear-gradient(90deg, rgba(99,102,241,0.05), rgba(99,102,241,0.12), rgba(99,102,241,0.05))",
                            "backgroundSize": "200% 100%",
                            "animation": "shimmer 1.5s ease-in-out infinite",
                            "borderRadius": "5px", "marginBottom": "8px",
                        }),
                        html.Div(style={
                            "height": "10px", "width": "70%",
                            "background": "linear-gradient(90deg, rgba(99,102,241,0.04), rgba(99,102,241,0.10), rgba(99,102,241,0.04))",
                            "backgroundSize": "200% 100%",
                            "animation": "shimmer 1.5s ease-in-out infinite 0.2s",
                            "borderRadius": "5px", "marginBottom": "8px",
                        }),
                        html.Div(style={
                            "height": "10px", "width": "90%",
                            "background": "linear-gradient(90deg, rgba(99,102,241,0.03), rgba(99,102,241,0.08), rgba(99,102,241,0.03))",
                            "backgroundSize": "200% 100%",
                            "animation": "shimmer 1.5s ease-in-out infinite 0.4s",
                            "borderRadius": "5px",
                        }),
                        html.P("🔄 Generating AI analysis...", style={
                            "color": THEME["text_muted"], "fontSize": FONT["xs"],
                            "marginTop": "12px", "fontWeight": "500",
                        }),
                    ], style={"minHeight": "80px"}),
                ],
            ),
        ], style={"padding": "22px 26px"}),
    ], style=glass_card({
        "overflow": "hidden", "padding": "0",
        "border": "1px solid rgba(99,102,241,0.12)",
        "margin": "0 20px 18px 20px",
    }))
