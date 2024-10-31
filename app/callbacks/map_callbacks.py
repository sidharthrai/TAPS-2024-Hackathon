# app/callbacks/map_callbacks.py
from dash.dependencies import Input, Output
from app import app
from data_loader_custom.data_loader import load_plot_boundaries
import plotly.graph_objects as go
import numpy as np
import random
# Load GeoDataFrame for plotting
geo_df, unique_blocks, unique_treatments = load_plot_boundaries()


@app.callback(
    Output('map', 'figure'),
    Input('block-filter', 'value'),
    Input('treatments-checklist', 'value')
)
def update_map(selected_blocks, selected_treatments):
    fig = go.Figure()
    filtered_geo_df = geo_df[geo_df['Block_ID'].isin(selected_blocks)]
    filtered_geo_df = filtered_geo_df[filtered_geo_df['TRT_ID'].isin(selected_treatments)]
    colors = {
        1: "blue",
        2: "yellow",
        3: "red",
        4: "green"
    }

    # Track which blocks have already been added to the legend
    blocks_added_to_legend = set()

    for _, row in filtered_geo_df.iterrows():
        lats, lons = np.array(row['geometry'].exterior.xy[1]), np.array(row['geometry'].exterior.xy[0])
        
        # Show legend only for the first occurrence of each block
        show_legend = row['Block_ID'] not in blocks_added_to_legend
        if show_legend:
            blocks_added_to_legend.add(row['Block_ID'])

        fig.add_trace(go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='lines',
            fill='toself',
            name=f"Block {row['Block_ID']}" if show_legend else "",  # Name only on the first occurrence
            showlegend=show_legend,  # Show legend only once per block
            fillcolor=colors[row['Block_ID']],
            line=dict(width=1, color='black'),
            text=f"TRT_ID: {row['TRT_ID']}",
            hoverinfo='text'
        ))

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center={"lat": geo_df.geometry.centroid.y.mean(), "lon": geo_df.geometry.centroid.x.mean()},
            zoom=16,
        ),
        margin={"r":0, "t":0, "l":0, "b":0},
        legend=dict(
        itemclick=False,          # Disables single click to toggle visibility
        itemdoubleclick=False      # Disables double-click to isolate trace
    )
    )
    return fig