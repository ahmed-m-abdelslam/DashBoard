import dash
from dash import dcc, html
from threading import Timer
import subprocess
import platform

from config import APP_PORT, APP_HOST, APP_DEBUG, THEME
from components.upload import make_upload_section
from components.topbar import make_topbar
from callbacks.upload_callback import register_upload_callback
from callbacks.fullscreen_callback import register_fullscreen_callback


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

    register_upload_callback(app)
    register_fullscreen_callback(app)

    return app


def open_browser(url):
    try:
        system = platform.system().lower()
        if system == "linux":
            for b in ["xdg-open", "google-chrome", "firefox"]:
                try:
                    subprocess.Popen([b, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return
                except FileNotFoundError:
                    continue
        elif system == "darwin":
            subprocess.Popen(["open", url])
        elif system == "windows":
            subprocess.Popen(["start", url], shell=True)
    except Exception:
        pass


if __name__ == "__main__":
    app = create_app()
    url = f"http://{APP_HOST}:{APP_PORT}"
    print(f"\n{'='*50}")
    print(f"  Dashboard: {url}")
    print(f"{'='*50}\n")
    Timer(2.0, open_browser, args=[url]).start()
    app.run(debug=APP_DEBUG, port=APP_PORT, host=APP_HOST)
