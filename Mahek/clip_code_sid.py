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
print('Inferno_r')


fig = go.Figure()

selected_plot = plot_boundary.index[0]
# Extract selected plot boundary
selected_boundary = plot_boundary.loc[[selected_plot], 'geometry']

# clip_fn = lambda polygon, R: R.rio.clip( [polygon.geometry], 
#                                     crs = R.rio.crs,
#                                     all_touched = True)

# Clip EC shallow and deep rasters to the selected plot boundary
ec_shallow_clipped = ec_shallow_da.rio.clip(selected_boundary.geometry, drop=True,all_touched = True)
ec_deep_clipped = ec_deep_da.rio.clip(selected_boundary.geometry, drop=True,all_touched = True)

# Plot EC Shallow
fig.add_trace(go.Heatmap(
    z=ec_shallow_clipped.values,
    x=ec_shallow_clipped.coords['x'].values,
    y=ec_shallow_clipped.coords['y'].values,
    colorscale="Inferno_r",
    colorbar=dict(title="EC Shallow"),
    zsmooth="best"
))


# Add plot boundary outline
boundary_x, boundary_y = list(selected_boundary.geometry.iloc[0].exterior.xy[0]), list(selected_boundary.geometry.iloc[0].exterior.xy[1])
fig.add_trace(go.Scatter(
    x=boundary_x,
    y=boundary_y,
    mode="lines",
    line=dict(color="black", width=2),
    name="Plot Boundary"
))

# Update layout
fig.update_layout(
    title=f"Clipped EC Data for Plot {selected_plot}",
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    template="plotly_white"
)
