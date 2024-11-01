from dash import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from app import app

from data_loader_custom.data_loader import crop_water_data

all_data = crop_water_data()

irrigation_data_long = pd.DataFrame({
    # Example data structure; replace with actual data source for irrigation data
    'Timestamp': pd.date_range(start='2023-01-01', periods=10),
    'Irrigation (inches)': [0.1, 0.3, 0.2, 0.5, 0.4, 0.2, 0.1, 0.3, 0.3, 0.2]
})

@app.callback(
        Output('crop_water_demand_graph', 'figure'),
        Input('crop_water_demand_graph', 'id')  # Triggered on app load
    )
def update_crop_water_demand_graph(_):
        fig = px.line(all_data, 
                      x='Timestamp', 
                      y='Crop Water Demand (mm/day)', 
                      color='Source',
                      title='Daily Crop Water Demand and Precipitation Across All Teams')

        for source in all_data['Source'].unique():
            fig.add_trace(
                go.Bar(x=all_data[all_data['Source'] == source]['Timestamp'],
                       y=all_data[all_data['Source'] == source]['Precipitation'],
                       opacity=0.6,
                       name=f"{source} - Precipitation")
            )

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Water (mm)',
            template='plotly_white',
            legend_title_text='Source',
            barmode='overlay'
        )

        return fig

@app.callback(
        Output('irrigation_graph', 'figure'),
        Input('irrigation_graph', 'id')  # Triggered on app load
    )
    def update_irrigation_graph(_):
        # Convert irrigation data from inches to mm if needed
        irrigation_data_long['Irrigation (mm)'] = irrigation_data_long['Irrigation (inches)'] * 25.4

        fig = px.bar(
            irrigation_data_long, 
            x='Timestamp', 
            y='Irrigation (mm)', 
            title='Irrigation Over Time (in mm)'
        )

        fig.update_traces(marker_color='darkgreen', opacity=0.8)
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Irrigation (mm)',
            template='plotly_white',
            yaxis=dict(range=[0, irrigation_data_long['Irrigation (mm)'].max() + 10]),
            xaxis=dict(tickangle=-45)
        )

        return fig
