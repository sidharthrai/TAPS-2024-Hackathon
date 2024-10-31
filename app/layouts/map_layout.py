# app/layouts/map_layout.py
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from data_loader_custom.data_loader import load_plot_boundaries

# Load data required for layout components
geo_df, unique_blocks, unique_treatments = load_plot_boundaries()

# Define filter components
block_filter_checklist = dbc.Checklist(
    id='block-filter',
    options=[{'label': str(block), 'value': block} for block in unique_blocks],
    value=unique_blocks
)

treatments_checklist = dbc.Checklist(
    id='treatments-checklist',
    options=[{'label': str(treatment), 'value': treatment} for treatment in unique_treatments],
    value=unique_treatments,
    inline=True
)

# Define layout
map_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Geospatial Plot Map", className="text-center mt-3 mb-4"))),
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
    ])
], fluid=True)
