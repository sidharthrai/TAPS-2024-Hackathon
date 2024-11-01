# app/data/data_loader.py
import pandas as pd
import geopandas as gpd
import numpy as np
import xarray as xr
from shapely.geometry import Point
from scipy.interpolate import griddata
import rioxarray  # For raster clipping

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

def load_plot_boundaries():
    path = '../Data/plot_boundaries/Map with all plots/2024_Colby_TAPS_Harvest_Area.shp'
    geo_df = gpd.read_file(path)
    # geo_df = gpd.read_file("../../Data/plot_boundaries/Map with all plots/2024_Colby_TAPS_Harvest_Area.shp")
    unique_blocks = geo_df['Block_ID'].unique()
    unique_treatments = sorted(geo_df['TRT_ID'].unique())
    return geo_df, unique_blocks, unique_treatments

def load_ec_data():
    ec_data = pd.read_excel("../Data/ec_data/2024_TAPS_Veris_raw_spatial_data.xlsx")
    geometry = [Point(xy) for xy in zip(ec_data['Long'], ec_data['Lat'])]
    ec_vector_data = gpd.GeoDataFrame(ec_data, geometry=geometry)
    ec_vector_data.set_crs("EPSG:4326", inplace=True)
    plot_boundary = load_plot_boundaries()[0]

    # Interpolate EC data
    points = np.array(list(zip(ec_vector_data.geometry.x, ec_vector_data.geometry.y)))
    ec_shallow = ec_vector_data['EC SH'].values
    ec_deep = ec_vector_data['EC DP'].values

    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()
    grid_x, grid_y = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    
    grid_z_shallow = griddata(points, ec_shallow, (grid_x, grid_y), method='cubic')
    grid_z_deep = griddata(points, ec_deep, (grid_x, grid_y), method='cubic')

    # Convert grid to xarray and clip
    ec_shallow_da = xr.DataArray(grid_z_shallow, dims=("y", "x"),
                                 coords={"y": np.linspace(y_min, y_max, grid_y.shape[1]),
                                         "x": np.linspace(x_min, x_max, grid_x.shape[0])})
    ec_deep_da = xr.DataArray(grid_z_deep, dims=("y", "x"), 
                          coords={"y": np.linspace(y_min, y_max, grid_y.shape[1]), 
                                  "x": np.linspace(x_min, x_max, grid_x.shape[0])})

    ec_shallow_da.rio.set_crs("EPSG:4326")
    ec_deep_da.rio.set_crs("EPSG:4326")

    # selected_boundary = plot_boundary.loc[plot_boundary, 'geometry']
    # ec_shallow_clipped = ec_shallow_da.rio.clip([selected_boundary], drop=True,all_touched = True)
    # ec_deep_clipped = ec_deep_da.rio.clip([selected_boundary], drop=True,all_touched = True)

    # boundary_x, boundary_y = list(selected_boundary.exterior.xy[0]), list(selected_boundary.exterior.xy[1])
    # boundary_x, boundary_y = list(selected_boundary.geometry.iloc[0].exterior.xy[0]), list(selected_boundary.geometry.iloc[0].exterior.xy[1])
    return ec_shallow_da, plot_boundary, ec_deep_da
    # return ec_shallow_clipped, ec_deep_clipped, boundary_x, boundary_y, plot_boundary






def load_arable_data():
    arable_data = pd.read_excel("../Data/sensor_data/24 KSU TAPS Arable.xlsx", sheet_name=None, skiprows=2)
    
    return arable_data




def soil_texture_data():
    soil_analysis = pd.read_excel("../Data/soil_analysis/24 KSU TAPS Soil texture.xlsx", skiprows=1)
    geometry = [Point(xy) for xy in zip(soil_analysis['Lng'], soil_analysis['Lat'])]
    soil_analysis_data = gpd.GeoDataFrame(soil_analysis, geometry=geometry)
    soil_analysis_data.set_crs("EPSG:4326", inplace=True)
    
    # Load plot boundary shapefile
    plot_boundary = gpd.read_file("../Data/plot_boundaries/Map with all plots/2024_Colby_TAPS_Harvest_Area.shx")

    # Interpolate EC Shallow and Deep
    points = np.array(list(zip(soil_analysis_data.geometry.x, soil_analysis_data.geometry.y)))
    soil_texture = soil_analysis_data['Soil Textural Class'].values

    #reclasify the values
    def soil_texture_reclasify(soil_texture):
        def reclassify(value):
            if value == 'Silty Clay Loam':
                return 1
            elif value == 'Silt Loam':
                return 2
            elif value == 'Clay Loam':
                return 3
            else:
                return 0
        reclassify_vectorized = np.vectorize(reclassify)
        reclassified_data = reclassify_vectorized(soil_texture)
        return reclassified_data
    
    
    soil_analysis_data['reclassified_soil_texture'] = soil_texture_reclasify(soil_texture)
    reclassify_soil_texture = soil_analysis_data['reclassified_soil_texture']
    
    
    # Define grid parameters for interpolation
    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()
    grid_x, grid_y = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]

    # Interpolated grids
    grid_z = griddata(points, reclassify_soil_texture, (grid_x, grid_y), method='cubic').astype(int)
    # grid_z_string = soil_texture_reverse_clasify(grid_z_values)
    # Convert interpolated grids to xarray DataArrays for clipping
    soil_texture_da = xr.DataArray(grid_z, dims=("y", "x"), 
                                coords={"y": np.linspace(y_min, y_max, grid_y.shape[1]), 
                                        "x": np.linspace(x_min, x_max, grid_x.shape[0])})

    # Set CRS to match the plot boundary CRS
    soil_texture_da.rio.set_crs("EPSG:4326")
    
    
    return soil_texture_da, plot_boundary
   
   
   