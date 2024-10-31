import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import geopandas as gpd
import os
import random
import numpy as np
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load shapefile with geopandas
shape_file_folder = "../Data/plot_boundaries/Map with all plots/"
shape_file_name = '2024_Colby_TAPS_Harvest_Area.shp'
shp_path = os.path.join(shape_file_folder, shape_file_name)
geo_df = gpd.read_file(shp_path)

# Assign random colors to each unique Block_ID
unique_blocks = geo_df['Block_ID'].unique()

colors = {block: f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})" for block in unique_blocks}

unique_treatments = geo_df['TRT_ID'].unique()
unique_treatments = sorted(unique_treatments)

# Create checklist for each group
treatments_checklist = dbc.Checklist(
        options=[{'label': str(treatment), 'value': treatment} for treatment in unique_treatments],
        id= "treatments-checklist",
        inline=True ,
        value=unique_treatments
        )


block_filter_checklist = dbc.Checklist(
                id='block-filter',
                options=[{'label': str(block), 'value': block} for block in unique_blocks],
                )



app.layout = dbc.Container([
    # Header
    dbc.Row(dbc.Col(html.H2("Geospatial Plot Map", className="text-center mt-3 mb-4"))),
    
    # Map and filters section
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Geospatial Map"),
                dbc.CardBody(dcc.Graph(id='map')),
            ]),
            width=9,
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Map Filters"),
                dbc.CardBody([
                    html.H5("Select Blocks", className="card-title"),
                    block_filter_checklist,
                    html.Hr(),
                    html.H5("Select Treatments", className="card-title"),
                    treatments_checklist
                ])
            ]),
            width=3,
        )
        
    ]),
    
    # Additional information/output section
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Map Information"),
                dbc.CardBody(html.Div(id='output')),
            ]),
            width=12,
            className="mt-4"
        )
    )
], fluid=True)




# Callback to update the map based on filter selection
@app.callback(
    Output('map', 'figure'),
    Input('block-filter', 'value'),
    Input('treatments-checklist', 'value')
)
def update_map(selected_blocks, selected_treatments):
    fig = go.Figure()
    
    # Filter GeoDataFrame if selection is made
    filtered_geo_df = geo_df[geo_df['Block_ID'].isin(selected_blocks)] if selected_blocks else geo_df
    filtered_geo_df = geo_df[geo_df['TRT_ID'].isin(selected_treatments)] if selected_treatments else geo_df
    
    # Create map polygons based on filtered data
    for _, row in filtered_geo_df.iterrows():
        coords = row['geometry'].exterior.coords.xy
        
        coords = row['geometry'].exterior.coords.xy
        lats = np.array(coords[1]).tolist()  # Convert to list
        lons = np.array(coords[0]).tolist()  # Convert to list

        fig.add_trace(go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='lines',
            fill='toself',
            name=f"Block ID {row['Block_ID']}",
            fillcolor=colors[row['Block_ID']],
            line=dict(width=1, color='black'),
            text=f"TRT_ID: {row['TRT_ID']}",
            hoverinfo='text',
            customdata=[row['TRT_ID']],
        ))
        
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center={"lat": geo_df.geometry.centroid.y.mean(), "lon": geo_df.geometry.centroid.x.mean()},
            zoom=16,
        ),
        margin={"r":0, "t":0, "l":0, "b":0},
        showlegend=False  # Disable legends
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
