from dash.dependencies import Input, Output, State
from app import app
import plotly.graph_objects as go
from data_loader_custom.data_loader import load_ec_data

# Load GeoDataFrame for plotting
ec_shallow_da, plot_boundary, ec_deep_da = load_ec_data()

# Function to update the shallow plot
def update_plot_shallow(selected_treatments):
    if not selected_treatments:
        return go.Figure()

    selected_boundary = plot_boundary[plot_boundary['TRT_ID'].isin(selected_treatments)]
    if selected_boundary.empty:
        return go.Figure()

    fig = go.Figure()
    for _, plot_row in selected_boundary.iterrows():
        clipped_shallow = ec_shallow_da.rio.clip([plot_row.geometry], drop=True, all_touched=True)
        fig.add_trace(go.Heatmap(
            z=clipped_shallow.values,
            x=clipped_shallow.coords['x'].values,
            y=clipped_shallow.coords['y'].values,
            colorscale="Inferno_r",
            showscale=False
        ))
        boundary_x, boundary_y = list(plot_row.geometry.exterior.xy[0]), list(plot_row.geometry.exterior.xy[1])
        fig.add_trace(go.Scatter(
            x=boundary_x, y=boundary_y,
            mode="lines", line=dict(color="black", width=2),
            name=f"Plot Boundary {plot_row['TRT_ID']}"
        ))

    fig.update_layout(
        title="Clipped EC Data - Shallow",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        template="plotly_white",
        showlegend=False
    )
    return fig

# Function to update the deep plot
def update_plot_deep(selected_treatments):
    if not selected_treatments:
        return go.Figure()

    selected_boundary = plot_boundary[plot_boundary['TRT_ID'].isin(selected_treatments)]
    if selected_boundary.empty:
        return go.Figure()

    fig = go.Figure()
    for _, plot_row in selected_boundary.iterrows():
        clipped_deep = ec_deep_da.rio.clip([plot_row.geometry], drop=True, all_touched=True)
        fig.add_trace(go.Heatmap(
            z=clipped_deep.values,
            x=clipped_deep.coords['x'].values,
            y=clipped_deep.coords['y'].values,
            colorscale="Inferno_r",
            showscale=False
        ))
        boundary_x, boundary_y = list(plot_row.geometry.exterior.xy[0]), list(plot_row.geometry.exterior.xy[1])
        fig.add_trace(go.Scatter(
            x=boundary_x, y=boundary_y,
            mode="lines", line=dict(color="black", width=2),
            name=f"Plot Boundary {plot_row['TRT_ID']}"
        ))

    fig.update_layout(
        title="Clipped EC Data - Deep",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        template="plotly_white",
        showlegend=False
    )
    return fig

# Define the callback to toggle between shallow and deep plot based on selected tab
@app.callback(
    Output("ec_plot_graph", "figure"),
    [Input("ec-tabs", "value")],
    [State("treatments-checklist", "value")]
)
def toggle_graph_display(selected_tab, selected_treatments):
    if selected_tab == "deep":
        return update_plot_deep(selected_treatments)
    return update_plot_shallow(selected_treatments)
