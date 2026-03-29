import dash
from dash import html, Output, Input, State
from ai.summaries import generate_portfolio_summary, generate_all_project_summaries
from config import THEME, FONT


def register_ai_callbacks(app):
    # ══════════════════════════════════════
    # Portfolio AI Summary — يحمّل بعد الداشبورد
    # ══════════════════════════════════════
    @app.callback(
        Output("ai-portfolio-content", "children"),
        Input("project-data-store", "data"),
        prevent_initial_call=True,
    )
    def load_portfolio_ai(store_data):
        if not store_data:
            return dash.no_update

        try:
            ai_text = generate_portfolio_summary(store_data)
            return html.Div([
                html.Div(style={
                    "height": "3px",
                    "background": "linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4, #6366f1)",
                    "backgroundSize": "300% 100%",
                    "animation": "gradient-shift 4s linear infinite",
                    "borderRadius": "4px", "marginBottom": "14px",
                }),
                html.Div(ai_text, style={
                    "fontSize": FONT["sm"], "lineHeight": "1.8",
                    "color": THEME["dark3"], "whiteSpace": "pre-line",
                }),
            ])
        except Exception:
            return html.P(
                "AI analysis could not be loaded.",
                style={"color": THEME["text_muted"], "fontSize": FONT["sm"]},
            )

    # ══════════════════════════════════════
    # Project Cards AI — يحمّل بعدين
    # ══════════════════════════════════════
    @app.callback(
        Output("ai-cards-container", "children"),
        Input("project-data-store", "data"),
        prevent_initial_call=True,
    )
    def load_project_ai(store_data):
        if not store_data:
            return dash.no_update

        try:
            summaries = generate_all_project_summaries(store_data)

            cards = []
            for name, summary in summaries.items():
                cards.append(html.Div([
                    html.H4(name, style={
                        "fontSize": FONT["sm"], "fontWeight": "700",
                        "color": THEME["indigo"], "margin": "0 0 6px 0",
                    }),
                    html.P(summary, style={
                        "fontSize": FONT["sm"], "color": THEME["dark3"],
                        "lineHeight": "1.7", "margin": "0",
                    }),
                ], style={
                    "backgroundColor": "rgba(238,242,255,0.6)",
                    "padding": "14px 16px", "borderRadius": "12px",
                    "border": "1px solid rgba(99,102,241,0.1)",
                    "marginBottom": "10px",
                }))

            return html.Div(cards)

        except Exception:
            return html.P(
                "AI project summaries could not be loaded.",
                style={"color": THEME["text_muted"], "fontSize": FONT["sm"]},
            )
