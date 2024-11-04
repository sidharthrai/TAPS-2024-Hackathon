# app/callbacks/map_callbacks.py
from dash.dependencies import Input, Output
from app import app
import plotly.graph_objects as go
from data_loader_custom.data_loader import load_arable_data

arable_data = load_arable_data()

@app.callback(
    Output("arable_crop_water_demand_over_time", "figure"),
    # [Input("collapse-crop_water_demand", "is_open")]
    # Input("crop_water_demand-toggle-button", "n_clicks")
    [Input("arable_crop_water_demand_over_time", "id")]
)
def arable_crop_water_demand_over_time(_):
    

    fig = go.Figure()


    for idx, key in enumerate(arable_data, start=2): 
        df = arable_data[key]
        fig.add_trace(go.Scatter(
            y=df["Arable Canopy Evapotranspiration (mm)"]+df["Arable Field Evapotranspiration (mm)"],
            x=df["Timestamp"],
            name=f'Treatment {idx}'
        ))
        # Customize layout
    fig.update_layout(
            title={'text': 'Arable: Soil Evapotranspiration Curve', 'x': 0.5},
            xaxis_title='Time',
            yaxis_title='Field Evapotranspiration (mm)')

    return fig