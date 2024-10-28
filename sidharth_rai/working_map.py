import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import shapefile as shp  # pyshp
import os 
# Initialize Dash app
import pandas as pd
app = dash.Dash(__name__)

# Load shapefile
shape_file_folder  = "../Data/plot_boundaries/Map with all plots/"
shape_file_name = '2024_Colby_TAPS_Harvest_Area.shp'
shp_path = os.path.join(shape_file_folder, shape_file_name)

sf = shp.Reader(shp_path)


# Extract polygons from shapefile
polygons = []
all_lats = []
all_lons = []

for shape in sf.shapes():
    polygon = shape.points
    polygons.append(polygon)
    lons, lats = zip(*polygon)
    all_lats.extend(lats)
    all_lons.extend(lons)

# Create a plotly figure
fig = go.Figure()

# Add each polygon to the figure
for i, polygon in enumerate(polygons):
    lons, lats = zip(*polygon)
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='lines',
        fill='toself',
        name=f'Plot {i+1}',  # Name for each plot
        customdata=[i+1] * len(lats),  # Set custom data to identify clicks
    ))

pth = '/Users/sidharthrai/Documents/hackathone_2024/Data/ec_data/2024_TAPS_Veris_raw_spatial_data.xlsx'
df = pd.read_excel(pth)

fig.add_trace(go.Scattermapbox(
    lon=df['Long'],
    lat=df['Lat'],
    mode='markers',
    marker=dict(size=8, color=df['Temp'], colorscale='Viridis', showscale=True),
    text=df.apply(lambda row: f"Temp: {row['Temp']}°F, Altitude: {row['Altitude']}m, Speed: {row['Speed']} m/s", axis=1),
    hoverinfo='text'
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
        plot_id = clickData['points'][0]['customdata']
        return f'You clicked on Plot {plot_id}'
    return 'Click on a plot to see details.'

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)