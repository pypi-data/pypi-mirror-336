# gradient_flow_interactive.py

import numpy as np
import webbrowser
import threading
from time import sleep
from matplotlib import cm as cm
from matplotlib import colors as mcolors

# Dash imports cho chế độ WebView
import dash
from dash import dcc, html, Input, Output

# ======================================================
# Facade: Tool wrapper that packages Model, Visualizer and UIController
# ======================================================
class GradientFlowInteractive:
    def __init__(self, debug_folder):
        self.model = GradientModel(debug_folder)
        self.visualizer = Visualizer(self.model)
        self.ui_controller = UIController(self.model, self.visualizer)

    def render_ipywidgets(self):
        """Render the tool using ipywidgets (for Jupyter Notebook)."""
        self.ui_controller.render_ui()

    def render_webview(self, port=8050):
        """
        Render the tool in a standalone web browser window using Dash.
        The local URL will be printed to the console.
        """
        # Create a Dash app to host a minimal interface (demo purpose)
        app = dash.Dash(__name__)

        # Initial sankey figure from current settings
        sankey_fig = self.visualizer.create_sankey(
            self.ui_controller.layer_dropdown.value,
            self.ui_controller.node_slider.value,
            self.ui_controller.threshold_slider.value,
            self.ui_controller.region_settings,
            self.model.selectable_layers
        )

        app.layout = html.Div([
            html.H1("Gradient Flow Interactive Tool"),
            html.Div("Local URL: http://127.0.0.1:" + str(port)),
            dcc.Graph(id="sankey-graph", figure=sankey_fig),
            html.Label("Threshold:", style={'fontWeight': 'bold'}),
            dcc.Slider(
                id="threshold-slider",
                min=self.model.flow_threshold_min,
                max=self.model.flow_threshold_max,
                step=(self.model.flow_threshold_max - self.model.flow_threshold_min) / 100,
                value=self.ui_controller.threshold_slider.value,
                marks={round(i, 1): str(round(i, 1)) for i in np.linspace(self.model.flow_threshold_min, self.model.flow_threshold_max, 5)}
            )
        ])

        @app.callback(
            Output("sankey-graph", "figure"),
            Input("threshold-slider", "value")
        )
        def update_sankey(threshold):
            fig = self.visualizer.create_sankey(
                self.ui_controller.layer_dropdown.value,
                self.ui_controller.node_slider.value,
                threshold,
                self.ui_controller.region_settings,
                self.model.selectable_layers
            )
            fig.update_layout(title_text=f"Gradient Flow (Threshold: {threshold})")
            return fig

        # Run the Dash app in a separate thread so as not to block the main thread.
        def run_dash():
            app.run_server(port=port, debug=False)

        dash_thread = threading.Thread(target=run_dash)
        dash_thread.daemon = True
        dash_thread.start()

        local_url = f"http://127.0.0.1:{port}"
        print("WebView is available at:", local_url)
        # Optionally, open the browser automatically
        try:
            # Give the server a short time to start
            sleep(1)
            webbrowser.open(local_url)
        except Exception as e:
            print("Could not open the web browser automatically. Please open the URL manually.")