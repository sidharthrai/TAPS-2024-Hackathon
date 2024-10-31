# app/callbacks/map_callbacks.py
from dash.dependencies import Input, Output
from app import app
from data_loader_custom.data_loader import load_ec_data
import plotly.graph_objects as go

# Load GeoDataFrame for plotting
# ec_shallow_clipped,ec_deep_clipped,  boundary_x, boundary_y, plot_boundary =  load_ec_data()

ec_shallow_da, plot_boundary,ec_deep_da = load_ec_data()




# Callback for updating the plot
@app.callback(
    Output("ec_plot_shallow", "figure"),
    # Input("ec_plot", "id")  # Dummy input to trigger loading the plot
    Input('treatments-checklist', 'value')

)
def update_plot(selected_treatments):
    if not selected_treatments:
        return go.Figure()

    # Filter plot_boundary for the selected TRT_ID
    selected_boundary = plot_boundary[plot_boundary['TRT_ID'].isin(selected_treatments)]
    
    if selected_boundary.empty:
        return go.Figure()
    
    fig = go.Figure()

    # Loop through each plot boundary to clip and add to the figure
    for _, plot_row in selected_boundary.iterrows():
        # Clip EC shallow and deep rasters to each plot boundary
        clipped_shallow = ec_shallow_da.rio.clip([plot_row.geometry], drop=True, all_touched=True)

        # Plot EC Shallow for each plot boundary
        fig.add_trace(go.Heatmap(
            z=clipped_shallow.values,
            x=clipped_shallow.coords['x'].values,
            y=clipped_shallow.coords['y'].values,
            colorscale="Inferno_r",
            colorbar=dict(title="EC Shallow"),
            zsmooth="best",
            showscale=False  # Disable individual color bars for each plot
        ))

        # Add plot boundary outline
        boundary_x, boundary_y = list(plot_row.geometry.exterior.xy[0]), list(plot_row.geometry.exterior.xy[1])
        fig.add_trace(go.Scatter(
            x=boundary_x,
            y=boundary_y,
            mode="lines",
            line=dict(color="black", width=2),
            name=f"Plot Boundary {plot_row['TRT_ID']}"
        ))

    # Update layout
    fig.update_layout(
        title="Clipped EC Data for All Plots",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        template="plotly_white",
        showlegend=False
    )

    return fig





# Callback for updating the plot
@app.callback(
    Output("ec_plot_deep", "figure"),
    # Input("ec_plot", "id")  # Dummy input to trigger loading the plot
    Input('treatments-checklist', 'value')

)
def update_plot(selected_treatments):
    if not selected_treatments:
        return go.Figure()

    # Filter plot_boundary for the selected TRT_ID
    selected_boundary = plot_boundary[plot_boundary['TRT_ID'].isin(selected_treatments)]
    
    if selected_boundary.empty:
        return go.Figure()
    
    fig = go.Figure()

    # Loop through each plot boundary to clip and add to the figure
    for _, plot_row in selected_boundary.iterrows():
        # Clip EC shallow and deep rasters to each plot boundary
        clipped_shallow = ec_deep_da.rio.clip([plot_row.geometry], drop=True, all_touched=True)

        # Plot EC Shallow for each plot boundary
        fig.add_trace(go.Heatmap(
            z=clipped_shallow.values,
            x=clipped_shallow.coords['x'].values,
            y=clipped_shallow.coords['y'].values,
            colorscale="Inferno_r",
            colorbar=dict(title="EC Shallow"),
            zsmooth="best",
            showscale=False  # Disable individual color bars for each plot
        ))

        # Add plot boundary outline
        boundary_x, boundary_y = list(plot_row.geometry.exterior.xy[0]), list(plot_row.geometry.exterior.xy[1])
        fig.add_trace(go.Scatter(
            x=boundary_x,
            y=boundary_y,
            mode="lines",
            line=dict(color="black", width=2),
            name=f"Plot Boundary {plot_row['TRT_ID']}"
        ))

    # Update layout
    fig.update_layout(
        title="Clipped EC Data for All Plots",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        template="plotly_white",
        showlegend=False
    )

    return fig
