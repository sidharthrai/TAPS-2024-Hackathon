import callbacks.map_callbacks 
import callbacks.ec_callbacks
import callbacks.arable_crop_water_demand_callbacks
from app import app
from dash import Dash
import dash_bootstrap_components as dbc
from layouts.map_layout import map_layout
# from layouts.ec_plot import ec_plot
from layouts.ec_layout import ec_layout
from layouts.arable_crop_water_demand_layout import crop_water_layout
import dash
# import callbacks.graph_callbacks  # Load graph callbacks

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = dbc.Container([map_layout, ec_plot, graphs], fluid=True)

dash.register_page(__name__, path='/')

app.layout = dbc.Container([map_layout, ec_layout,crop_water_layout], fluid=True)

