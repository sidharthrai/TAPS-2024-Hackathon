from dash import Dash
import dash_bootstrap_components as dbc
from layouts.map_layout import map_layout
# from layouts.ec_plot import ec_plot
from layouts.ec_layout import ec_layout
# from layouts.graphs import graphs
from app import app

import callbacks.map_callbacks  # Load map callbacks
import callbacks.ec_callbacks
# import callbacks.graph_callbacks  # Load graph callbacks

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = dbc.Container([map_layout, ec_plot, graphs], fluid=True)
app.layout = dbc.Container([map_layout, ec_layout], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
