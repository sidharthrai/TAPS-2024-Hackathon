# import dash
# from dash import dcc, html, Input, Output
# import geopandas as gpd
# import plotly.graph_objects as go
# import rioxarray  # For raster clipping
# from scipy.interpolate import griddata
# import numpy as np
# import xarray as xr
# import pandas as pd
# from shapely.geometry import Point

# # Initialize the app
# app = dash.Dash(__name__)

# # Load EC data and create GeoDataFrame
# ec_data = pd.read_excel("../Data/ec_data/2024_TAPS_Veris_raw_spatial_data.xlsx")
# geometry = [Point(xy) for xy in zip(ec_data['Long'], ec_data['Lat'])]
# ec_vector_data = gpd.GeoDataFrame(ec_data, geometry=geometry)
# ec_vector_data.set_crs("EPSG:4326", inplace=True)

# # Load plot boundary shapefile
# plot_boundary = gpd.read_file("../Data/plot_boundaries/Map with all plots/2024_Colby_TAPS_Harvest_Area.shx")

# # Interpolate EC Shallow and Deep
# points = np.array(list(zip(ec_vector_data.geometry.x, ec_vector_data.geometry.y)))
# ec_shallow = ec_vector_data['EC SH'].values
# ec_deep = ec_vector_data['EC DP'].values

# # Define grid parameters for interpolation
# x_min, x_max = points[:, 0].min(), points[:, 0].max()
# y_min, y_max = points[:, 1].min(), points[:, 1].max()
# grid_x, grid_y = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]

# # Interpolated grids
# grid_z_shallow = griddata(points, ec_shallow, (grid_x, grid_y), method='cubic')
# grid_z_deep = griddata(points, ec_deep, (grid_x, grid_y), method='cubic')

# # Convert interpolated grids to xarray DataArrays for clipping
# ec_shallow_da = xr.DataArray(grid_z_shallow, dims=("y", "x"), 
#                              coords={"y": np.linspace(y_min, y_max, grid_y.shape[1]), 
#                                      "x": np.linspace(x_min, x_max, grid_x.shape[0])})
# ec_deep_da = xr.DataArray(grid_z_deep, dims=("y", "x"), 
#                           coords={"y": np.linspace(y_min, y_max, grid_y.shape[1]), 
#                                   "x": np.linspace(x_min, x_max, grid_x.shape[0])})

# # Set CRS to match the plot boundary CRS
# ec_shallow_da.rio.set_crs("EPSG:4326")
# ec_deep_da.rio.set_crs("EPSG:4326")

# # Get unique TRT_ID values for dropdown
# trt_ids = plot_boundary['TRT_ID'].unique()

# # Layout
# app.layout = html.Div([
#     dcc.Dropdown(
#         id="trt_id_selector",
#         options=[{"label": trt_id, "value": trt_id} for trt_id in trt_ids],
#         placeholder="Select TRT_ID",
#     ),
#     dcc.Graph(id="ec_plot")
# ])

# # Callback for updating the plot
# @app.callback(
#     Output("ec_plot", "figure"),
#     Input("trt_id_selector", "value")
# )
# def update_plot(selected_id):
#     if not selected_id:
#         return go.Figure()

#     # Filter plot_boundary for the selected TRT_ID
#     selected_boundary = plot_boundary[plot_boundary['TRT_ID'] == selected_id]
#     if selected_boundary.empty:
#         return go.Figure()

#     # Clip EC shallow and deep rasters to the selected plot boundary
#     ec_shallow_clipped = ec_shallow_da.rio.clip(selected_boundary.geometry, drop=True, all_touched=True)
#     ec_deep_clipped = ec_deep_da.rio.clip(selected_boundary.geometry, drop=True, all_touched=True)

#     # Create figure
#     fig = go.Figure()

#     # Plot EC Shallow
#     fig.add_trace(go.Heatmap(
#         z=ec_shallow_clipped.values,
#         x=ec_shallow_clipped.coords['x'].values,
#         y=ec_shallow_clipped.coords['y'].values,
#         colorscale="Inferno_r",
#         colorbar=dict(title="EC Shallow"),
#         zsmooth="best"
#     ))

#     # Add plot boundary outline
#     boundary_x, boundary_y = list(selected_boundary.geometry.iloc[0].exterior.xy[0]), list(selected_boundary.geometry.iloc[0].exterior.xy[1])
#     fig.add_trace(go.Scatter(
#         x=boundary_x,
#         y=boundary_y,
#         mode="lines",
#         line=dict(color="black", width=2),
#         name="Plot Boundary"
#     ))

#     # Update layout
#     fig.update_layout(
#         title=f"Clipped EC Data for TRT_ID {selected_id}",
#         xaxis_title="Longitude",
#         yaxis_title="Latitude",
#         template="plotly_white"
#     )

#     return fig

# # Run the app
# if __name__ == "__main__":
#     app.run_server(debug=True)


import dash
from dash import dcc, html, Input, Output
import geopandas as gpd
import plotly.graph_objects as go
import rioxarray  # For raster clipping
from scipy.interpolate import griddata
import numpy as np
import xarray as xr
import pandas as pd
from shapely.geometry import Point

# Initialize the app
app = dash.Dash(__name__)

# Load EC data and create GeoDataFrame
ec_data = pd.read_excel("../Data/ec_data/2024_TAPS_Veris_raw_spatial_data.xlsx")
geometry = [Point(xy) for xy in zip(ec_data['Long'], ec_data['Lat'])]
ec_vector_data = gpd.GeoDataFrame(ec_data, geometry=geometry)
ec_vector_data.set_crs("EPSG:4326", inplace=True)

# Load plot boundary shapefile
plot_boundary = gpd.read_file("../Data/plot_boundaries/Map with all plots/2024_Colby_TAPS_Harvest_Area.shx")

# Interpolate EC Shallow and Deep
points = np.array(list(zip(ec_vector_data.geometry.x, ec_vector_data.geometry.y)))
ec_shallow = ec_vector_data['EC SH'].values
ec_deep = ec_vector_data['EC DP'].values

# Define grid parameters for interpolation
x_min, x_max = points[:, 0].min(), points[:, 0].max()
y_min, y_max = points[:, 1].min(), points[:, 1].max()
grid_x, grid_y = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]

# Interpolated grids
grid_z_shallow = griddata(points, ec_shallow, (grid_x, grid_y), method='cubic')
grid_z_deep = griddata(points, ec_deep, (grid_x, grid_y), method='cubic')

# Convert interpolated grids to xarray DataArrays for clipping
ec_shallow_da = xr.DataArray(grid_z_shallow, dims=("y", "x"), 
                             coords={"y": np.linspace(y_min, y_max, grid_y.shape[1]), 
                                     "x": np.linspace(x_min, x_max, grid_x.shape[0])})
ec_deep_da = xr.DataArray(grid_z_deep, dims=("y", "x"), 
                          coords={"y": np.linspace(y_min, y_max, grid_y.shape[1]), 
                                  "x": np.linspace(x_min, x_max, grid_x.shape[0])})

# Set CRS to match the plot boundary CRS
ec_shallow_da.rio.set_crs("EPSG:4326")
ec_deep_da.rio.set_crs("EPSG:4326")

# Layout
app.layout = html.Div([
    dcc.Graph(id="ec_plot")
])

# Callback for updating the plot
@app.callback(
    Output("ec_plot", "figure"),
    Input("ec_plot", "id")  # Dummy input to trigger loading the plot
)
def show_all_plots(_):
    # Create figure
    fig = go.Figure()

    # Loop through each plot boundary to clip and add to the figure
    for _, plot_row in plot_boundary.iterrows():
        # Clip EC shallow and deep rasters to each plot boundary
        clipped_shallow = ec_shallow_da.rio.clip([plot_row.geometry], drop=True, all_touched=True)

        # Plot EC Shallow for each plot boundary
        fig.add_trace(go.Heatmap(
            z=clipped_shallow.values,
            x=clipped_shallow.coords['x'].values,
            y=clipped_shallow.coords['y'].values,
            colorscale="Inferno_r",
            colorbar=dict(title="EC Shallow"),
            zsmooth="best",
            showscale=False  # Disable individual color bars for each plot
        ))

        # Add plot boundary outline
        boundary_x, boundary_y = list(plot_row.geometry.exterior.xy[0]), list(plot_row.geometry.exterior.xy[1])
        fig.add_trace(go.Scatter(
            x=boundary_x,
            y=boundary_y,
            mode="lines",
            line=dict(color="black", width=2),
            name=f"Plot Boundary {plot_row['TRT_ID']}"
        ))

    # Update layout
    fig.update_layout(
        title="Clipped EC Data for All Plots",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        template="plotly_white"
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
