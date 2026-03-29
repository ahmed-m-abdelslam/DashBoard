import os
import dash
from dash import dcc, html

from config import THEME
from components.upload import make_upload_section
from components.topbar import make_topbar
from callbacks.upload_callback import register_upload_callback
from callbacks.fullscreen_callback import register_fullscreen_callback
from callbacks.ai_callback import register_ai_callbacks


def create_app():
    app = dash.Dash(
        __name__,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
            {"name": "theme-color", "content": "#0f172a"},
        ],
        suppress_callback_exceptions=True,
    )

    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>Luxury Hospitality - Procurement Dashboard</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
            {%favicon%}
            {%css%}
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    app.layout = html.Div([
        dcc.Store(id="project-data-store", storage_type="memory"),
        dcc.Loading(
            id="main-loading",
            type="circle",
            color="#6366f1",
            fullscreen=True,
            style={"backgroundColor": "rgba(15,23,42,0.5)"},
            children=[
                make_upload_section(),
                html.Div(
                    id="dashboard-section",
                    style={"display": "none"},
                    children=[
                        make_topbar(),
                        html.Div(id="dashboard-body"),
                    ],
                ),
            ],
        ),
    ], id="main-container", style={
        "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
        "backgroundImage": "url('/assets/background.jpg')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "backgroundRepeat": "no-repeat",
        "backgroundAttachment": "fixed",
        "minHeight": "100vh",
    })

    # Register callbacks
    register_upload_callback(app)
    register_fullscreen_callback(app)
    register_ai_callbacks(app)  # ← جديد

    return app


app = create_app()
server = app.server


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    print(f"\n{'='*50}")
    print(f"  Dashboard: http://0.0.0.0:{port}")
    print(f"{'='*50}\n")
    app.run(debug=debug, port=port, host="0.0.0.0")
