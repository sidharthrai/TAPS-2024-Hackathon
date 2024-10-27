#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:42:36 2024

@author: mahek
"""

import numpy as np
import pandas as pd
import matplotlib as plt
 
#Reading the arable data
arable_team_2 = pd.read_excel("/Users/mahek/hackathon/Sensor Data/24 KSU TAPS Arable.xlsx", sheet_name="Team #2 Data")







#Calculating field capacity for different plots based on soil texture
soil_texture = pd.read_excel("/Users/mahek/hackathon/Soil Analysis/24 KSU TAPS Soil texture.xlsx",skiprows=1)
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

soil_texture.FC = 100*field_capacity((soil_texture.Sand_/100), (soil_texture.Clay_/100), (soil_texture.OMC_/100))   
