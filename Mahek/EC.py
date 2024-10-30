#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:02:10 2024

@author: mahek
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
import xarray as xr
import matplotlib.pyplot as plt
from shapely.geometry import Point
from scipy.interpolate import griddata
from rasterio.transform import from_origin

#Reading the EC data
ec_data = pd.read_excel("../Data/ec_data/2024_TAPS_Veris_raw_spatial_data.xlsx")
 
# generating a geodatabase from excel data
geometry = [Point(xy) for xy in zip(ec_data['Long'], ec_data['Lat'])]

# Create a GeoDataFrame
ec_vector_data = gpd.GeoDataFrame(ec_data, geometry=geometry)
ec_vector_data.set_crs("EPSG:4326", inplace=True) 
ec_vector_data.to_file('EC_vector_file.geojson', driver="GeoJSON")

#Interpolating the data
points = np.array(list(zip(ec_vector_data.geometry.x, ec_vector_data.geometry.y)))
ec_shallow = ec_vector_data['EC SH'].values
ec_deep = ec_vector_data['EC DP'].values

#Define grid parameters
x_min, x_max = points[:, 0].min(), points[:, 0].max()
y_min, y_max = points[:, 1].min(), points[:, 1].max()
grid_x, grid_y = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]

#Interpolate data to the grid
grid_z_shallow = griddata(points, ec_shallow, (grid_x, grid_y), method='cubic') #cubic interpolation
grid_z_deep = griddata(points, ec_deep, (grid_x, grid_y), method='cubic') #cubic interpolation


#writing the raster file for EC shallow and deep
with rasterio.open('Interpolated_raster_EC_shallow.tif', 'w', driver= 'GTiff', 
                   height= 200, width= 200,
                   count= 1, crs = "EPSG:4326", dtype= grid_z_shallow.dtype,
                   transform = from_origin(x_min, y_max, (x_max - x_min) /100 , (y_max - y_min) /100)) as dst:
    dst.write(grid_z_shallow,1)

ec_raster_shallow = xr.open_dataarray("interpolated_raster_EC_shallow.tif") 


#Plotting the EC shallow data   
plt.figure(figsize=(8,6))
ec_raster_shallow.plot(cmap='inferno_r', vmax=60, vmin=0)
plt.title('EC Shallow')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
    
with rasterio.open('Interpolated_raster_EC_deep.tif', 'w', driver= 'GTiff', 
                   height= grid_z_deep.shape[0], width= grid_z_deep.shape[1],
                   count= 1, crs = "EPSG:4326", dtype= grid_z_deep.dtype,
                   transform = from_origin(x_min, y_max, (x_max - x_min) /100 , (y_max - y_min) /100)) as dst:
    dst.write(grid_z_deep,1)

ec_raster_deep = xr.open_dataarray("interpolated_raster_EC_deep.tif") 

 #Plotting the EC deep data     
plt.figure(figsize=(8,6))
ec_raster_deep.plot(cmap='inferno_r', vmax=60, vmin=0)
plt.title('EC Deep')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

#Clipping the EC values by plt boundary
plot_boundary = gpd.read_file("../Data/plot_boundaries/Map with all plots/2024_Colby_TAPS_Harvest_Area.shx")


#Define function for cliping raster file to tuttle creek
clip_fn = lambda polygon, R: R.rio.clip( [polygon.geometry], 
                                        crs = R.rio.crs,
                                        all_touched = True)


#Clip the EC values to plot boundary
plot_boundary['EC_shallow'] = plot_boundary.apply(lambda row: clip_fn(row,ec_raster_shallow), axis =1)
plot_boundary.head(3)

plot_boundary['EC_deep'] = plot_boundary.apply(lambda row: clip_fn(row,ec_raster_deep), axis =1)
plot_boundary.head(3)


                                
#Plotting the EC values 
fig,ax = plt.subplots(figsize = (10,8))
plot_boundary.loc[ [0], 'geometry'].boundary.plot(ax=ax, edgecolor = 'k', linewidth=8)
plot_boundary.loc[0, 'EC_shallow'].plot(ax=ax, cmap='inferno_r')
ax.set_title('EC Shallow')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude') 
plt.show()

fig,ax = plt.subplots(figsize = (10,8))
plot_boundary.loc[ [0], 'geometry'].boundary.plot(ax=ax, edgecolor = 'k', linewidth=8)
plot_boundary.loc[0, 'EC_deep'].plot(ax=ax, cmap='inferno_r')
ax.set_title('EC Deep')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.show()
