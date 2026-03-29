import pandas as pd
from dash import html, dash_table
from config import THEME, FONT
from data.utils import status_color, risk_color, urgency_color
from components.shared import section_title, glass_card


def make_data_table(all_data):
    rows = []
    for d in all_data:
        rows.append({
            "Project": d.get("project_name", ""),
            "Stage": d.get("current_stage", ""),
            "Opening": d.get("opening_date", "TBD"),
            "Urgency": d.get("urgency_category", "TBD"),
            "Currency": d.get("currency", ""),
            "Budget": f"{d['effective_budget']:,.0f}",
            "Committed": f"{d['committed_spend']:,.0f}",
            "Util %": f"{d['budget_utilization_pct']:.0f}%",
            "Variance": f"{d['budget_variance']:+,.0f}",
            "Pkgs": f"{int(d['packages_completed'])}/{int(d['total_packages'])}",
            "POs Del": f"{int(d['delivered_pos'])}/{int(d['total_pos'])}",
            "Del Rate": f"{d['po_delivery_rate']:.0f}%",
            "Completion": f"{d['overall_completion']:.0f}%",
            "SPI": f"{d.get('schedule_performance_index', 1):.2f}",
            "Risk": f"{d['risk_score']}",
        })
    df_table = pd.DataFrame(rows)

    style_cond = [
        {"if": {"row_index": "odd"}, "backgroundColor": "rgba(248,250,252,0.5)"},
        {"if": {"state": "active"}, "backgroundColor": "rgba(99,102,241,0.06)", "border": "none"},
    ]
    for i, d in enumerate(all_data):
        style_cond.append({"if": {"row_index": i, "column_id": "Risk"}, "color": risk_color(d["risk_score"]), "fontWeight": "800"})
        style_cond.append({"if": {"row_index": i, "column_id": "Variance"}, "color": THEME["success"] if d["budget_variance"] >= 0 else THEME["danger"], "fontWeight": "800"})
        style_cond.append({"if": {"row_index": i, "column_id": "Completion"}, "color": status_color(d["overall_completion"]), "fontWeight": "800"})
        style_cond.append({"if": {"row_index": i, "column_id": "Urgency"}, "color": urgency_color(d.get("urgency_category", "TBD")), "fontWeight": "800"})

    return html.Div([
        section_title("Project Summary Table"),
        html.Div([
            dash_table.DataTable(
                data=df_table.to_dict("records"),
                columns=[{"name": c, "id": c} for c in df_table.columns],
                style_table={"overflowX": "auto", "borderRadius": "14px"},
                style_header={
                    "backgroundColor": THEME["dark"],
                    "color": "#fff",
                    "fontWeight": "700",
                    "fontSize": FONT["sm"],
                    "textAlign": "center",
                    "padding": "14px 10px",
                    "fontFamily": "Inter",
                    "borderBottom": "2px solid rgba(99,102,241,0.3)",
                    "letterSpacing": "0.2px",
                },
                style_cell={
                    "textAlign": "center",
                    "padding": "12px 10px",
                    "fontSize": FONT["sm"],
                    "fontFamily": "Inter",
                    "border": "none",
                    "borderBottom": f"1px solid rgba(226,232,240,0.5)",
                    "minWidth": "72px",
                    "color": THEME["text"],
                    "transition": "background-color 0.2s ease",
                },
                style_data_conditional=style_cond,
                sort_action="native",
                filter_action="native",
                page_size=20,
            )
        ], style=glass_card({
            "overflow": "hidden", "padding": "0",
            "border": "1px solid rgba(226,232,240,0.5)",
        })),
    ], style={"padding": "0 20px 18px 20px"})
