#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:42:36 2024

@author: mahek
"""

import numpy as np
import pandas as pd
import plotly.express as px
 
#Reading the arable data
arable_team_2 = pd.read_excel("../Data/sensor_data/24 KSU TAPS Arable.xlsx", sheet_name="Team #2 Data", skiprows=2)
arable_team_2.columns = arable_team_2.columns.str.replace(' ','')
arable_team_2.columns = arable_team_2.columns.str.replace('(mm)','')






#Calculating field capacity for different plots based on soil texture
soil_texture = pd.read_excel("../Data/soil_analysis/24 KSU TAPS Soil texture.xlsx",skiprows=1)
soil_texture.columns = soil_texture.columns.str.replace('(%)', '_')
soil_texture.columns = soil_texture.columns.str.replace(' ', '')

# field capacity = coeff + (1.283*(coeff**2)-0.374*coeff-0.015)
# coeff = -0.251*sand +0.195*clay +0.011*OM + 0.006(sand*OM)-0.027(clay*OM)+0.452(sand*clay)+0.078

def field_capacity(sand, clay, OM):
    """"
    field capacity = amount of water available to plants which is based on soil texture at 33KPa (%volume)
    Sand = percentage of sand content (%weight)
    Clay = percentage of clay content (%weight)
    Organic Matter (OM) = percentage of organic matter (%weight)
    Reference for the formula Saxton and Rawls,2006
    (https://acsess.onlinelibrary.wiley.com/doi/full/10.2136/sssaj2005.0117)
    """""
    #sand, clay, OM = float(sand, clay, OM)
    coeff = -0.251*sand + 0.195*clay +0.011*OM + 0.006*(sand*OM)-0.027*(clay*OM)+0.452*(sand*clay)+0.078
    field_capac = coeff + (1.283*(coeff**2)-(0.374*coeff)-0.015)
    return field_capac

field_capacity = 100*field_capacity((soil_texture.Sand_/100), (soil_texture.Clay_/100), (soil_texture.OMC_/100))   


Crop_water_demand = arable_team_2.ArableCanopyEvapotranspiration + arable_team_2.ArableFieldEvapotranspiration
Precip = arable_team_2.Precipitation*arable_team_2.PrecipitationHours
data = pd.DataFrame()
data['Time_Stamp'] = arable_team_2.Timestamp.copy()
data['crop_demand'] = Crop_water_demand.copy()
data['Precip'] = Precip.copy()

fig = px.scatter(data, x='Time_Stamp', y='crop_demand', title='Crop Water Demand Over Time')
fig.show()



