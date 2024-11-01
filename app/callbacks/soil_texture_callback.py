    # app/callbacks/map_callbacks.py
from dash.dependencies import Input, Output
from app import app
import plotly.graph_objects as go
import numpy as np
import random
import rioxarray
from data_loader_custom.data_loader import soil_texture_data    
    
# @app.callback(
#     Output('soil_texture_map', 'figure'),
#     Input('block-filter_soil', 'value'),
#     Input('treatments-checklist_soil', 'value')
# )
# def update_soil_texture_map(selected_blocks, selected_treatments):
    
#     fig = go.Figure()

#     # Filter plots by selected blocks and treatments
#     filtered_geo_df = plot_boundary[plot_boundary['Block_ID'].isin(selected_blocks)]
#     selected_plots = filtered_geo_df[filtered_geo_df['TRT_ID'].isin(selected_treatments)]

#     # Ensure at least one plot is selected
#     if not selected_plots.empty:
#         # Assuming selecting the first plot in the filtered data
#         selected_boundary = selected_plots.iloc[0]['geometry']

#         # Clip soil texture data to the selected plot boundary
#         soil_texture_clipped = soil_texture_da.rio.clip([selected_boundary], drop=True, all_touched=True)
        
#         # Plot clipped soil texture as heatmap
#         fig.add_trace(go.Heatmap(
#             z=soil_texture_clipped.values,
#             x=soil_texture_clipped.coords['x'].values,
#             y=soil_texture_clipped.coords['y'].values,
#             colorscale="ylorbr",
#             colorbar=dict(title="Soil Texture"),
#             zsmooth="best"
#         ))

#         # Extract and add plot boundary outline
#         boundary_x, boundary_y = list(selected_boundary.exterior.xy[0]), list(selected_boundary.exterior.xy[1])
#         fig.add_trace(go.Scatter(
#             x=boundary_x,
#             y=boundary_y,
#             mode="lines",
#             line=dict(color="black", width=2),
#             name="Plot Boundary"
#         ))

#     # Update layout with titles
#     fig.update_layout(
#         title="Clipped Soil Texture for Selected Plot",
#         xaxis_title="Longitude",
#         yaxis_title="Latitude",
#         template="plotly_white"
#     )
    
#     return fig


# Traceback (most recent call last):
#   File "/Users/sidharthrai/Documents/hackathone_2024/app/callbacks/soil_texture_callback.py", line 75, in update_soil_texture_map
#     selected_boundary = plot_boundary[plot_boundary['TRT_ID'].isin(selected_treatments)]
# UnboundLocalError: local variable 'plot_boundary' referenced before assignment

@app.callback(
    Output('soil_texture_map', 'figure'),
    Input('block-filter_soil', 'value'),
    Input('treatments-checklist_soil', 'value')
)
def update_soil_texture_map(selected_blocks, selected_treatments):
    fig = go.Figure()
    soil_texture_da, plot_boundary = soil_texture_data()

    # Check if any treatments are selected
    if not selected_treatments:
        return fig  # Return an empty figure if no treatments are selected

    # Filter the plot boundaries by selected treatments
    selected_boundary = plot_boundary[plot_boundary['TRT_ID'].isin(selected_treatments)]
    
    # Return an empty figure if no boundaries match the selected treatments
    if selected_boundary.empty:
        return fig

    # Ensure both soil_texture_da and plot_boundary have the same CRS
    if soil_texture_da.rio.crs != plot_boundary.crs:
        plot_boundary = plot_boundary.to_crs(soil_texture_da.rio.crs)

    # Loop through each selected plot boundary
    for _, plot_row in selected_boundary.iterrows():
        try:
            # Slightly expand bounds by buffering to ensure overlap
            buffered_geometry = plot_row.geometry.buffer(0.0001)  # Adjust buffer size as needed

            # Clip the soil texture data to the buffered plot boundary
            soil_texture_clipped = soil_texture_da.rio.clip([buffered_geometry], drop=True, all_touched=True)

            # Add heatmap trace for the clipped soil texture data
            fig.add_trace(go.Heatmap(
                z=soil_texture_clipped.values,
                x=soil_texture_clipped.coords['x'].values,
                y=soil_texture_clipped.coords['y'].values,
                colorscale="ylorbr",
                showscale=False  # Set to False to avoid multiple colorbars
            ))

            # Add boundary outline for the current plot
            boundary_x, boundary_y = list(plot_row.geometry.exterior.xy[0]), list(plot_row.geometry.exterior.xy[1])
            fig.add_trace(go.Scatter(
                x=boundary_x, 
                y=boundary_y,
                mode="lines",
                line=dict(color="black", width=2),
                name=f"Plot Boundary {plot_row['TRT_ID']}"
            ))

        except rioxarray.exceptions.NoDataInBounds:
            # Skip this plot if no data is found within the bounds
            print(f"No data found in bounds for plot {plot_row['TRT_ID']}")

    # Update layout with titles and styling
    fig.update_layout(
        title="Soil Texture Map with Selected Plot Boundaries",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        template="plotly_white",
        showlegend=False
    )

    return fig