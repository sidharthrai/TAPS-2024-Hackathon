# app/layouts/map_layout.py
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from data_loader_custom.data_loader import load_ec_data
from app import app




ec_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("EC Plot", className="text-center mt-3 mb-4"))),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("EC Plot Shallow"),
                dbc.CardBody(dcc.Graph(id='ec_plot_shallow')),
            ]),
            width=12,
        )]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("EC Plot Deep"),
                dbc.CardBody(dcc.Graph(id='ec_plot_deep')),
            ]),
            width=12,
        )]),
    
    ], fluid=True)
        
