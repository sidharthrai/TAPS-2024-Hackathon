from dash import Output, Input
import plotly.graph_objs as go
from app import app
from data_loader_custom.data_loader import aqua_spy_data
aqua_spy = aqua_spy_data()

@app.callback(
        Output("moisture_graph", "figure"),
        Input("team_dropdown", "value"),
        Input("depth_dropdown", "value")
    )
def update_graph(selected_team, selected_depths):
        df = aqua_spy[selected_team]  # Select data for the chosen team
        fig = go.Figure()

        for depth in selected_depths:
            fig.add_trace(go.Scatter(
                y=df[depth],
                x=df["Timestamp"],
                mode='lines',
                name=f"{selected_team} - {depth} Depth"
            ))

        fig.update_layout(
            width=1200, height=500,
            title={'text': f'Soil Moisture measured by Aqua Spy - {selected_team}', 'x': 0.5},
            xaxis_title='Time',
            yaxis_title='Soil Moisture (%)'
        )

        return fig
