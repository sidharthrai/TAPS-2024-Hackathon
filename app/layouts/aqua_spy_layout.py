from dash import dcc, html
import dash_bootstrap_components as dbc
from data_loader_custom.data_loader import aqua_spy_data

aqua_spy = aqua_spy_data()


depths = ["4\"", "8\"", "12\"", "16\"", "20\"", "24\"", "28\"", "32\"", "36\"", "40\"", "44\"", "48\""]
teams = list(aqua_spy.keys())

aqua_spy_lay =  dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Soil Moisture Dashboard"),
                dcc.Dropdown(
                    id="team_dropdown",
                    options=[{"label": team, "value": team} for team in teams],
                    value=teams[0],  # Default value
                    clearable=False,
                    placeholder="Select Team"
                ),
                dcc.Dropdown(
                    id="depth_dropdown",
                    options=[{"label": depth, "value": depth} for depth in depths],
                    value=depths[:1],  # Default value: First depth
                    multi=True,
                    placeholder="Select Depth(s)"
                ),
            ], width=3),
            dbc.Col([
                dcc.Graph(id="moisture_graph", style={'height': '500px'})
            ], width=9)
        ])
    ])