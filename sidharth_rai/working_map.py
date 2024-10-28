import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import shapefile as shp  # pyshp
import os 
# Initialize Dash app
import geopandas as gpd

import random

app = dash.Dash(__name__)

# Load shapefile
shape_file_folder  = "../Data/plot_boundaries/Map with all plots/"
shape_file_name = '2024_Colby_TAPS_Harvest_Area.shp'
shp_path = os.path.join(shape_file_folder, shape_file_name)

sf = shp.Reader(shp_path)
geo_df = gpd.read_file(shp_path)


# Extract polygons from shapefile
polygons = []
all_lats = []
all_lons = []
polygons_by_trt = {}

for i,shape in enumerate(sf.shapes()):
    polygon = shape.points

    polygons.append({
        'polygon': polygon,
        'Block_ID': geo_df['Block_ID'][i],
        'TRT_ID': geo_df['TRT_ID'][i]
    })
    
    trt_id = geo_df['TRT_ID'][i]
    # if trt_id not in polygons:
    #     polygons[trt_id] = [] 
    
    # polygons[trt_id].append(polygon)
    
    lons, lats = zip(*polygon)
    all_lats.extend(lats)
    all_lons.extend(lons)

# Create a plotly figure
fig = go.Figure()
# Assign random colors to each unique Block_ID
unique_blocks = set([poly['Block_ID'] for poly in polygons])
colors = {block: f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})" for block in unique_blocks}


# Add each polygon to the figure
for i, poly_data in enumerate(polygons):
    
    polygon = poly_data['polygon']
    block_id = poly_data['Block_ID']
    trt_id = poly_data['TRT_ID']
    
    lons, lats = zip(*polygon)
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='lines',
        fill='toself',
        name=f'TRT_ID {trt_id}',  # Name for each plot
        fillcolor=colors[block_id],
        line=dict(width=1, color='black'),
        text=f"TRT_ID: {trt_id}",  # Text with TRT_ID
        hoverinfo='text',
        customdata=[trt_id] * len(lats),  # Set custom data to identify clicks
    ))



# Configure map layout, centering based on the dataset’s extent
fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center={"lat": sum(all_lats) / len(all_lats), "lon": sum(all_lons) / len(all_lons)},
        zoom=12  # Adjust zoom as necessary
    ),
    margin={"r":0,"t":0,"l":0,"b":0}
)

# Dash app layout
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig),
    html.Div(id='output')
])

# Callback to display info when a plot is clicked
@app.callback(
    Output('output', 'children'),
    [Input('map', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        trt_id = clickData['points'][0]['customdata']
        return f'You clicked on TRT_ID {trt_id}'
    return 'Click on a plot to see details.'

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)