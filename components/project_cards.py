import plotly.graph_objects as go
from dash import html, dcc
from config import THEME, FONT, PROJECT_COLORS
from data.utils import hex_to_rgba, fmt_num, status_color, risk_color, urgency_color
from components.shared import glass_card, make_progress_bar, kpi_chip, status_badge, concern_badge


def _make_single_card(data, pc_idx, ai_summary=""):
    pc = PROJECT_COLORS[pc_idx % len(PROJECT_COLORS)]
    name = data["project_name"]
    currency = data["currency"]
    budget = data["effective_budget"]
    overall = data["overall_completion"]
    risk_score = data["risk_score"]
    concerns = data["concerns"]
    oc = status_color(overall)
    rc = risk_color(risk_score)
    uc = urgency_color(data.get("urgency_category", "TBD"))

    # Gauge
    gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=round(overall, 1),
        number={"suffix": "%", "font": {"size": 32, "color": pc["main"], "family": "Inter", "weight": 800}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 9, "color": "#94a3b8"}, "dtick": 25},
            "bar": {"color": oc, "thickness": 0.75},
            "bgcolor": "rgba(241,245,249,0.5)", "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": hex_to_rgba(THEME["danger"], 0.04)},
                {"range": [40, 75], "color": hex_to_rgba(THEME["warning"], 0.04)},
                {"range": [75, 100], "color": hex_to_rgba(THEME["success"], 0.04)},
            ],
        },
    ))
    gauge.update_layout(height=135, margin=dict(t=10, b=0, l=18, r=18), paper_bgcolor="rgba(0,0,0,0)")

    # Waterfall
    ordered = data["orders_placed"]
    in_prog = data["orders_in_progress"]
    remaining = max(0, budget - ordered - in_prog)
    wf = go.Figure(go.Waterfall(
        orientation="v",
        x=["Budget", "Ordered", "In Progress", "Remaining"],
        y=[budget, -ordered, -in_prog, 0],
        measure=["absolute", "relative", "relative", "total"],
        text=[fmt_num(v, currency) for v in [budget, ordered, in_prog, remaining]],
        textposition="outside", textfont=dict(size=10, family="Inter", weight=600),
        connector={"line": {"color": "rgba(0,0,0,0.04)", "width": 1}},
        increasing={"marker": {"color": pc["main"], "line": {"width": 0}}},
        decreasing={"marker": {"color": THEME["warning"], "line": {"width": 0}}},
        totals={"marker": {"color": THEME["success"] if remaining >= 0 else THEME["danger"], "line": {"width": 0}}},
    ))
    wf.update_layout(
        height=195, margin=dict(t=20, b=30, l=38, r=14),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"}, showlegend=False,
        yaxis=dict(gridcolor="rgba(0,0,0,0.03)", tickfont={"size": 9}),
        xaxis=dict(tickfont={"size": 10, "weight": 600}),
    )

    sav = data["savings_overrun"]
    sav_color = THEME["success"] if sav >= 0 else THEME["danger"]
    proc_started = data.get("proc_started", "").lower() == "yes"
    del_started = data.get("delivery_started", "").lower() == "yes"
    cat_badges = [concern_badge(cat) for cat in data.get("concern_categories", [])]

    def section_label(text):
        return html.H4(text, style={
            "fontSize": FONT["sm"], "color": THEME["text"],
            "fontWeight": "800", "margin": "16px 0 10px 0",
            "letterSpacing": "-0.1px",
        })

    return html.Div([
        # ══════════════════════════════════════
        # HEADER
        # ══════════════════════════════════════
        html.Div([
            html.Div([
                html.H3(name, style={
                    "margin": "0", "color": "#fff", "fontSize": FONT["lg"],
                    "fontWeight": "800", "letterSpacing": "-0.3px",
                }),
                html.P(data["current_stage"], style={
                    "margin": "4px 0 0 0", "color": "rgba(255,255,255,0.65)",
                    "fontSize": FONT["xs"], "fontWeight": "500",
                }),
            ]),
            html.Div([
                html.Span(f"{risk_score}", style={
                    "fontSize": FONT["xl"], "fontWeight": "900", "color": "#fff",
                    "lineHeight": "1",
                }),
                html.Span("RISK", style={
                    "fontSize": "8px", "color": "rgba(255,255,255,0.6)",
                    "textTransform": "uppercase", "letterSpacing": "1px",
                    "fontWeight": "700",
                }),
            ], style={
                "display": "flex", "flexDirection": "column", "alignItems": "center",
                "backgroundColor": hex_to_rgba(rc, 0.25),
                "padding": "8px 16px", "borderRadius": "12px",
                "border": "1px solid rgba(255,255,255,0.15)",
                "backdropFilter": "blur(10px)",
            }),
        ], style={
            "display": "flex", "justifyContent": "space-between", "alignItems": "center",
            "background": pc["gradient"], "padding": "18px 22px",
            "borderRadius": "16px 16px 0 0",
            "position": "relative", "overflow": "hidden",
        }),

        # ══════════════════════════════════════
        # BODY
        # ══════════════════════════════════════
        html.Div([
            # Status badges
            html.Div([
                status_badge("Procurement", proc_started),
                status_badge("Delivery", del_started),
                html.Span(f"📅 {data['opening_date']}", style={
                    "fontSize": "10px", "fontWeight": "600", "color": THEME["info"],
                    "backgroundColor": hex_to_rgba(THEME["info"], 0.06),
                    "padding": "4px 10px", "borderRadius": "20px",
                    "border": f"1px solid {hex_to_rgba(THEME['info'], 0.12)}",
                }),
                html.Span(data.get("urgency_category", "TBD"), style={
                    "fontSize": "10px", "fontWeight": "700", "color": uc,
                    "backgroundColor": hex_to_rgba(uc, 0.08),
                    "padding": "4px 10px", "borderRadius": "20px",
                    "border": f"1px solid {hex_to_rgba(uc, 0.12)}",
                }),
            ], style={"display": "flex", "gap": "6px", "flexWrap": "wrap", "marginBottom": "14px"}),

            # KPIs
            html.Div([
                kpi_chip("Budget", fmt_num(budget, currency), "💰", pc["main"]),
                kpi_chip("Savings" if sav >= 0 else "Overrun", fmt_num(abs(sav), currency), "📊", sav_color),
                kpi_chip("Util", f"{data['budget_utilization_pct']:.0f}%", "📈", THEME["info"]),
            ], style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "16px"}),

            # Gauge
            section_label("Overall Completion"),
            html.Div(
                dcc.Graph(figure=gauge, config={"displayModeBar": False}),
                className="gauge-container",
                style={
                    "backgroundColor": "rgba(248,250,252,0.6)",
                    "borderRadius": "12px", "padding": "6px 0",
                    "marginBottom": "14px",
                    "border": "1px solid rgba(226,232,240,0.4)",
                },
            ),

            # Progress bars
            section_label("Progress Tracking"),
            html.Div([
                make_progress_bar("Packages Completed", data["packages_completed"], data["total_packages"], THEME["success"]),
                make_progress_bar("Packages In Progress", data["packages_in_progress"], data["total_packages"], THEME["warning"]),
                make_progress_bar("POs Delivered", data["delivered_pos"], data["total_pos"], THEME["info"]),
            ], style={
                "backgroundColor": "rgba(248,250,252,0.6)",
                "padding": "16px", "borderRadius": "12px",
                "marginBottom": "14px",
                "border": "1px solid rgba(226,232,240,0.4)",
            }),

            # Advanced Metrics
            section_label("Advanced Metrics"),
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("SPI", style={"fontSize": "9px", "color": THEME["text_muted"], "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                        html.Span(f"{data.get('schedule_performance_index', 1):.2f}", style={
                            "fontSize": FONT["lg"], "fontWeight": "900",
                            "color": THEME["success"] if data.get("schedule_performance_index", 1) >= 0.9 else THEME["danger"],
                        }),
                    ], style={"textAlign": "center", "flex": "1", "padding": "4px 0"}),
                    html.Div(style={"width": "1px", "backgroundColor": "rgba(226,232,240,0.5)", "alignSelf": "stretch"}),
                    html.Div([
                        html.Span("Pipeline", style={"fontSize": "9px", "color": THEME["text_muted"], "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                        html.Span(f"{data['pipeline_closure_rate']:.0f}%", style={"fontSize": FONT["lg"], "fontWeight": "900", "color": THEME["purple"]}),
                    ], style={"textAlign": "center", "flex": "1", "padding": "4px 0"}),
                    html.Div(style={"width": "1px", "backgroundColor": "rgba(226,232,240,0.5)", "alignSelf": "stretch"}),
                    html.Div([
                        html.Span("Del. Rate", style={"fontSize": "9px", "color": THEME["text_muted"], "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                        html.Span(f"{data['po_delivery_rate']:.0f}%", style={
                            "fontSize": FONT["lg"], "fontWeight": "900",
                            "color": THEME["success"] if data["po_delivery_rate"] >= 60 else THEME["danger"],
                        }),
                    ], style={"textAlign": "center", "flex": "1", "padding": "4px 0"}),
                    html.Div(style={"width": "1px", "backgroundColor": "rgba(226,232,240,0.5)", "alignSelf": "stretch"}),
                    html.Div([
                        html.Span("Gap", style={"fontSize": "9px", "color": THEME["text_muted"], "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                        html.Span(f"{data['delivery_gap']:.0f}pp", style={"fontSize": FONT["lg"], "fontWeight": "900", "color": THEME["orange"]}),
                    ], style={"textAlign": "center", "flex": "1", "padding": "4px 0"}),
                ], style={
                    "display": "flex", "padding": "14px 10px",
                    "backgroundColor": "rgba(248,250,252,0.6)",
                    "borderRadius": "12px",
                    "border": "1px solid rgba(226,232,240,0.4)",
                }),
            ], style={"marginBottom": "14px"}),

            # Waterfall
            section_label("Budget Breakdown"),
            html.Div(
                dcc.Graph(figure=wf, config={"displayModeBar": False}),
                className="waterfall-container",
                style={
                    "backgroundColor": "rgba(248,250,252,0.6)",
                    "borderRadius": "12px", "marginBottom": "14px",
                    "border": "1px solid rgba(226,232,240,0.4)",
                },
            ),

            # Concerns
            section_label("Concerns & Risk Categories"),
            html.Div(cat_badges, style={
                "display": "flex", "gap": "5px", "flexWrap": "wrap", "marginBottom": "10px",
            }) if cat_badges else html.Div(),

            html.Div([
                html.Div(c, className="concern-item", style={
                    "padding": "10px 14px",
                    "backgroundColor": "rgba(255,251,235,0.8)",
                    "borderRadius": "10px", "fontSize": FONT["sm"],
                    "borderLeft": f"3px solid {THEME['warning']}",
                    "marginBottom": "6px", "color": "#92400e",
                    "lineHeight": "1.6", "transition": "all 0.2s ease",
                }) for c in concerns
            ]) if concerns else html.P("No concerns reported", style={
                "color": THEME["success"], "fontSize": FONT["sm"], "margin": "0",
                "padding": "10px 14px",
                "backgroundColor": hex_to_rgba(THEME["success"], 0.04),
                "borderRadius": "10px",
                "borderLeft": f"3px solid {THEME['success']}",
                "fontWeight": "600",
            }),

            # ══════════════════════════════════════
            # AI SUMMARY — هنا بالظبط التعديل
            # ══════════════════════════════════════
            html.Div([
                html.H4("AI Analysis", style={
                    "fontSize": FONT["sm"], "color": THEME["text"],
                    "fontWeight": "800", "margin": "16px 0 10px 0",
                }),
                html.Div([
                    html.Div(style={
                        "height": "2px",
                        "background": "linear-gradient(90deg, #6366f1, #8b5cf6, transparent)",
                        "borderRadius": "2px", "marginBottom": "12px",
                    }),
                    html.Div(
                        ai_summary if ai_summary else "See AI Insights section below ↓",
                        style={
                            "fontSize": FONT["sm"],
                            "color": "#3730a3" if ai_summary else THEME["text_muted"],
                            "lineHeight": "1.7",
                            "fontStyle": "normal" if ai_summary else "italic",
                        },
                    ),
                ], style={
                    "backgroundColor": "rgba(238,242,255,0.6)",
                    "padding": "14px 16px", "borderRadius": "12px",
                    "border": "1px solid rgba(99,102,241,0.1)",
                }),
            ]),
            # ══════════════════════════════════════

        ], style={"padding": "18px 22px"}),  # ← إغلاق الـ BODY div

    ], className="project-card", style=glass_card({
        "overflow": "hidden", "flex": "1",
        "minWidth": "400px", "maxWidth": "560px",
        "border": "1px solid rgba(226,232,240,0.5)",
    }))


# ══════════════════════════════════════════════════
# الدوال الجديدة للـ Placeholder (بدون AI)
# ══════════════════════════════════════════════════

def _make_card_without_ai(data, pc_idx):
    """Same card but without AI summary — shows placeholder text."""
    return _make_single_card(data, pc_idx, ai_summary="")


def make_project_cards_section(all_data, ai_summaries=None):
    """Full version with AI summaries (used if AI is pre-loaded)."""
    if ai_summaries is None:
        ai_summaries = {}

    cards = []
    for i, d in enumerate(all_data):
        summary = ai_summaries.get(d["project_name"], "")
        cards.append(_make_single_card(d, i, summary))

    return html.Div([
        html.Div([
            html.H2("Project Detail Cards", className="section-title", style={
                "fontSize": FONT["lg"], "color": THEME["text"], "fontWeight": "800",
                "margin": "0 0 20px 0", "paddingBottom": "12px",
                "borderBottom": f"2px solid {THEME['border']}",
            }),
        ], style={"padding": "0 20px"}),
        html.Div(cards, style={
            "display": "flex", "justifyContent": "center",
            "alignItems": "flex-start", "gap": "20px",
            "flexWrap": "wrap", "padding": "0 20px 40px 20px",
        }),
    ])


def make_project_cards_section_placeholder(all_data):
    """Fast version — cards without AI, AI loads separately below."""
    cards = []
    for i, d in enumerate(all_data):
        cards.append(_make_card_without_ai(d, i))

    return html.Div([
        # Project cards (instant)
        html.Div([
            html.H2("Project Detail Cards", className="section-title", style={
                "fontSize": FONT["lg"], "color": THEME["text"], "fontWeight": "800",
                "margin": "0 0 20px 0", "paddingBottom": "12px",
                "borderBottom": f"2px solid {THEME['border']}",
            }),
        ], style={"padding": "0 20px"}),

        html.Div(cards, style={
            "display": "flex", "justifyContent": "center",
            "alignItems": "flex-start", "gap": "20px",
            "flexWrap": "wrap", "padding": "0 20px 20px 20px",
        }),

        # AI Insights section (loads async via callback)
        html.Div([
            html.H2("AI Project Insights", className="section-title", style={
                "fontSize": FONT["lg"], "color": THEME["text"], "fontWeight": "800",
                "margin": "0 0 20px 0", "paddingBottom": "12px",
                "borderBottom": f"2px solid {THEME['border']}",
            }),
            html.Div(
                id="ai-cards-container",
                children=[
                    html.Div([
                        # Shimmer loading skeleton
                        html.Div(style={
                            "height": "12px", "width": "60%",
                            "background": "linear-gradient(90deg, rgba(99,102,241,0.05), rgba(99,102,241,0.12), rgba(99,102,241,0.05))",
                            "backgroundSize": "200% 100%",
                            "animation": "shimmer 1.5s ease-in-out infinite",
                            "borderRadius": "6px", "marginBottom": "10px",
                        }),
                        html.Div(style={
                            "height": "12px", "width": "80%",
                            "background": "linear-gradient(90deg, rgba(99,102,241,0.04), rgba(99,102,241,0.10), rgba(99,102,241,0.04))",
                            "backgroundSize": "200% 100%",
                            "animation": "shimmer 1.5s ease-in-out infinite 0.3s",
                            "borderRadius": "6px", "marginBottom": "10px",
                        }),
                        html.Div(style={
                            "height": "12px", "width": "45%",
                            "background": "linear-gradient(90deg, rgba(99,102,241,0.03), rgba(99,102,241,0.08), rgba(99,102,241,0.03))",
                            "backgroundSize": "200% 100%",
                            "animation": "shimmer 1.5s ease-in-out infinite 0.6s",
                            "borderRadius": "6px",
                        }),
                        html.P("🔄 Generating AI insights for each project...", style={
                            "color": THEME["text_muted"], "fontSize": FONT["xs"],
                            "fontWeight": "500", "marginTop": "14px",
                        }),
                    ], style={"minHeight": "80px"}),
                ],
            ),
        ], style={"padding": "0 20px 40px 20px"}),
    ])
