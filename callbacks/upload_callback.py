import dash
from dash import html, Output, Input, State
from data.parser import parse_file, ParseError
from components.portfolio_header import make_portfolio_header
from components.ai_section import make_ai_portfolio_section_placeholder
from components.progress_charts import make_progress_analysis
from components.budget_charts import make_budget_analysis
from components.pipeline_charts import make_procurement_pipeline
from components.delivery_charts import make_delivery_analysis
from components.risk_charts import make_risk_analysis
from components.timeline_charts import make_timeline_analysis
from components.data_table import make_data_table
from components.project_cards import make_project_cards_section_placeholder
from config import THEME
import json


def register_upload_callback(app):
    @app.callback(
        Output("upload-section", "style"),
        Output("dashboard-section", "style"),
        Output("dashboard-body", "children"),
        Output("upload-error", "children"),
        Output("project-data-store", "data"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        prevent_initial_call=True,
    )
    def handle_upload(contents, filename):
        if contents is None:
            return (
                dash.no_update, dash.no_update,
                dash.no_update, "", dash.no_update,
            )

        try:
            all_data = parse_file(contents, filename)
        except ParseError as e:
            return (
                dash.no_update, dash.no_update, dash.no_update,
                html.P(str(e), style={"color": THEME["danger"], "fontWeight": "600"}),
                dash.no_update,
            )
        except Exception as e:
            return (
                dash.no_update, dash.no_update, dash.no_update,
                html.P(f"Error: {str(e)}", style={"color": THEME["danger"]}),
                dash.no_update,
            )

        # ══════════════════════════════════════════════
        # Build dashboard WITHOUT AI — فوري
        # ══════════════════════════════════════════════
        body = html.Div([
            make_portfolio_header(all_data),
            make_ai_portfolio_section_placeholder(),
            make_progress_analysis(all_data),
            make_budget_analysis(all_data),
            make_procurement_pipeline(all_data),
            make_delivery_analysis(all_data),
            make_risk_analysis(all_data),
            make_timeline_analysis(all_data),
            make_data_table(all_data),
            make_project_cards_section_placeholder(all_data),
        ])

        # Store data for lazy AI loading
        # Remove non-serializable fields
        store_data = []
        for d in all_data:
            clean = {k: v for k, v in d.items() if k != "opening_date_parsed"}
            store_data.append(clean)

        return (
            {"display": "none"},
            {"display": "block"},
            body,
            "",
            store_data,
        )
