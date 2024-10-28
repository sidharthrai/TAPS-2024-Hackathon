import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

pth = '/Users/sidharthrai/Documents/hackathone_2024/Data/ec_data/2024_TAPS_Veris_raw_spatial_data.xlsx'
df = pd.read_excel(pth)


# Initialize Dash app
app = dash.Dash(__name__)

# Create a plotly figure
fig = go.Figure()

# Add scatter points to the map
fig.add_trace(go.Scattermapbox(
    lon=df['Long'],
    lat=df['Lat'],
    mode='markers',
    marker=dict(size=8, color=df['Temp'], colorscale='Viridis', showscale=True),
    text=df.apply(lambda row: f"Temp: {row['Temp']}°F, Altitude: {row['Altitude']}m, Speed: {row['Speed']} m/s", axis=1),
    hoverinfo='text'
))

# Configure map layout
fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center={"lat": df['Lat'].mean(), "lon": df['Long'].mean()},
        zoom=15  # Adjust zoom level as needed
    ),
    margin={"r":0, "t":0, "l":0, "b":0}
)

# Dash app layout
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)