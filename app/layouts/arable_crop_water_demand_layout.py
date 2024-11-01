import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from app import app
from data_loader_custom.data_loader import load_ec_data
from dash import  dcc
import dash_bootstrap_components as dbc
from dash import dcc, html

# Define custom styles for a prettier look
card_style = {
    "boxShadow": "0 4px 8px 0 rgb(228, 228, 228)",
    "border": "none",
    "marginBottom": "20px",
}
header_style = {
    "backgroundColor": "rgb(228, 228, 228)",
    "color": "black",
    "padding": "10px",
    "cursor": "pointer",
}
button_style = {
    "backgroundColor": "rgb(248, 248, 248)",
    "color": "#333",
    "fontSize": "18px",
    "textAlign": "center",
    "width": "100%",
    "borderRadius": "5px",
    "padding": "10px",
    "border": "2px solid rgb(228, 228, 228)",
    "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
    "outline": "none",
}

# Layout for Crop Water Demand Dashboard
crop_water_layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H2("Arable: Crop Water Demand Over Time Plot", className="text-center mt-3 mb-4"),
            style={"padding": "0", "margin": "0"}
        )
    ),
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    dbc.Button(
                        "Arable: Crop Water Demand Over Time Plot",
                        id="crop_water_demand-toggle-button",
                        style=button_style,
                    ),
                    style=header_style,
                ),
                dbc.Collapse(
                    dbc.CardBody(
                        dcc.Graph(
                            id='arable_crop_water_demand_over_time',
                            style={
                                "width": "90%",  # Adjust width to take 90% of the container width
                                "height": "90vh",  # Increase height for better visibility
                                "margin": "0 auto"  # Center the graph horizontally
                            }
                        )
                    ),
                    id="collapse-crop_water_demand",
                    is_open=True,
                    style={"transition": "height 0.4s ease-out"},
                ),
            ], style={**card_style, "width": "100%"}),  # Full width card
            width=12,
            style={"padding": "0", "margin": "0 auto", "display": "flex", "justify-content": "center"}
        )
    ),
], fluid=True, style={"padding": "0px"})  # Full width container with no padding




# Callback to toggle the Collapse component
@app.callback(
    Output("collapse-crop_water_demand", "is_open"),
    [Input("crop_water_demand-toggle-button", "n_clicks")],
    [State("collapse-crop_water_demand", "is_open")]
)
def toggle_shallow_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
