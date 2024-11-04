
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from data_loader_custom.data_loader import load_ec_data
from app import app
import plotly.express as px  # Assuming px is used for plotting


crop_water_layput = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Crop Water Demand",className="text-center mt-3 mb-4"),
                dcc.Graph(id='crop_water_demand_graph'),
                dcc.Graph(id='irrigation_graph')
            ])
        ]),
    ], fluid=True)
