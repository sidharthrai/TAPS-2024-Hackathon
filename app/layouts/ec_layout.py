from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from data_loader_custom.data_loader import load_ec_data
from app import app
import plotly.express as px  # Assuming px is used for plotting

# Define custom styles
card_style = {
    "boxShadow": "0 4px 8px 0 rgb(228, 228, 228)",
    "border": "none",
    "marginBottom": "20px",
}
tab_style = {
    "padding": "10px",
    "fontWeight": "bold",
    "backgroundColor": "rgb(248, 248, 248)",
    "border": "2px solid rgb(228, 228, 228)"
}
selected_tab_style = {
    "padding": "10px",
    "fontWeight": "bold",
    "backgroundColor": "rgb(220, 220, 220)"
}

# Layout with tabs and a single graph area
ec_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("EC Plot", className="text-center mt-3 mb-4"))),
    
    # Tabs for shallow and deep EC plots
    dbc.Row([
        dbc.Col(
            dcc.Tabs(
                id="ec-tabs",
                value='shallow',  # Default selected tab
                children=[
                    dcc.Tab(label="EC Plot Shallow", value="shallow", style=tab_style, selected_style=selected_tab_style),
                    dcc.Tab(label="EC Plot Deep", value="deep", style=tab_style, selected_style=selected_tab_style)
                ]
            ),
            width=12,
        )
    ], className="mb-3"),
    
    # Graph area that switches based on selected tab
    dbc.Row([
        dbc.Col(dcc.Graph(id='ec_plot_graph'), width=12)
    ])
], fluid=True)

