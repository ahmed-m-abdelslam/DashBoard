from dash import Output, Input


def register_fullscreen_callback(app):
    app.clientside_callback(
        """
        function(n1, n2) {
            var elem = document.getElementById('main-container');
            var triggered = dash_clientside.callback_context.triggered;
            if (!triggered || triggered.length === 0) return [window.dash_clientside.no_update, window.dash_clientside.no_update];
            var id = triggered[0].prop_id.split('.')[0];
            var enterBtn = document.getElementById('btn-fullscreen');
            var exitBtn = document.getElementById('btn-exit-fullscreen');
            if (id === 'btn-fullscreen') {
                if (elem.requestFullscreen) elem.requestFullscreen();
                else if (elem.webkitRequestFullscreen) elem.webkitRequestFullscreen();
                elem.style.overflow = 'auto'; elem.style.height = '100vh';
                if (enterBtn) enterBtn.style.display = 'none';
                if (exitBtn) exitBtn.style.display = 'flex';
            } else {
                if (document.exitFullscreen) document.exitFullscreen();
                else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
                elem.style.overflow = ''; elem.style.height = '';
                if (enterBtn) enterBtn.style.display = 'flex';
                if (exitBtn) exitBtn.style.display = 'none';
            }
            document.onfullscreenchange = function() {
                var e = document.getElementById('btn-fullscreen');
                var x = document.getElementById('btn-exit-fullscreen');
                var m = document.getElementById('main-container');
                if (!document.fullscreenElement) {
                    if (e) e.style.display='flex'; if (x) x.style.display='none';
                    m.style.overflow=''; m.style.height='';
                } else { m.style.overflow='auto'; m.style.height='100vh'; }
            };
            return [window.dash_clientside.no_update, window.dash_clientside.no_update];
        }
        """,
        Output("btn-fullscreen", "style"),
        Output("btn-exit-fullscreen", "style"),
        Input("btn-fullscreen", "n_clicks"),
        Input("btn-exit-fullscreen", "n_clicks"),
        prevent_initial_call=True,
    )
