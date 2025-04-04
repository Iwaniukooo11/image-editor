import dash
import dash_bootstrap_components as dbc
import sys
import os

core_path = os.path.abspath(os.path.join(os.getcwd(), 'core'))
sys.path.append(core_path)

pipeline_path = os.path.abspath(os.path.join(os.getcwd(), 'core', 'pipeline'))
sys.path.append(pipeline_path)

interfaces_path = os.path.abspath(os.path.join(os.getcwd(), 'core', 'interfaces'))
sys.path.append(interfaces_path)

filters_path = os.path.abspath(os.path.join(os.getcwd(), 'core', 'pipeline', 'filters'))
sys.path.append(filters_path)

convolutions_path = os.path.abspath(os.path.join(os.getcwd(), 'core', 'pipeline', 'convolutions'))
sys.path.append(convolutions_path)

edges_path = os.path.abspath(os.path.join(os.getcwd(), 'core', 'pipeline', 'edges'))
sys.path.append(edges_path)

callbacks_path = os.path.abspath(os.path.join(os.getcwd(), 'layout','callbacks'))
sys.path.append(callbacks_path)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True  # Allows dynamic callbacks
)
app.title = "Image Editor"

from layout.layout import create_layout
# from layout.callbacks.upload_image import register_callbacks as register_upload_callbacks
from layout.callbacks.callbacks import register_callbacks 


app.layout = create_layout()

register_callbacks(app)

if __name__ == "__main__":
    print("Starting Image Editor application...")
    app.run_server(debug=True)