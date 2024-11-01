from dash import Dash
import dash_bootstrap_components as dbc
from layouts.map_layout import map_layout
# from layouts.ec_plot import ec_plot
from layouts.ec_layout import ec_layout
# from layouts.graphs import graphs
from layouts.arable_crop_water_demand_layout import crop_water_layout
from layouts.soil_texture_layout import soil_texture_layout
from layouts.aqua_spy_layout import aqua_spy_lay
from app import app
from layouts.crop_water_demand_layout import crop_water_layput

import callbacks.map_callbacks 
import callbacks.ec_callbacks
import callbacks.arable_crop_water_demand_callbacks
import callbacks.aqua_spy_callback
import callbacks.crop_water_demand_call_back
# import callbacks.soil_texture_callback

# # import callbacks.graph_callbacks  # Load graph callbacks

# # app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# # app.layout = dbc.Container([map_layout, ec_plot, graphs], fluid=True)
app.layout = dbc.Container([map_layout, ec_layout,crop_water_layout,aqua_spy_lay,crop_water_layput], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
