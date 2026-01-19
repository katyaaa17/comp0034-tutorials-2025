import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dash_table, dcc, callback, input, output

# load the data
from src.mock_api import get_data, load_df
df = load_df()

# Create an instance of the Dash app, define the viewport meta tag and the external stylesheet
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

# Navbar component
navbar = dbc.Navbar(
    children=[
        dbc.Container(
            children=[
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row([
                        dbc.Col(html.Img(src=app.get_asset_url("logo.png"), height="40px")),
                        # dbc components use class_name=
                        dbc.Col(
                            dbc.NavbarBrand("Starfish data app", class_name="navbar-brand")),
                    ],
                    align="center",
                    ),
                    href="#",
                    style={"textDecoration": "none"},
                ),
            ],
            fluid=True
        ),
    ],
    color="black",
    dark=True,
)

# Chart filter
chart_selector = html.Div([
    html.Label("Select View:"),
    dbc.Select(
        id="chart-chooser",
        options=[
            {"label": "Species Distribution Map", "value": "map"},
            {"label": "Depth Analysis (Histogram)", "value": "bar"},
        ],
        value="map"
    ),
])

# Species filter
species_selector = html.Div([
    html.Label("Filter by Species:", className="mt-3"),
    dbc.Select(
        id="species-select",
        options=[
            {"label": "Asteroidea (All)", "value": "all"},
            {"label": "Common Starfish", "value": "common"},
            {"label": "Sun Star", "value": "sun"},
        ],
    ),
])

# Depth filter
depth_slider = html.Div([
    html.Label("Depth Range (meters):", className="mt-3"),
    dcc.RangeSlider(
        id="depth-slider",
        min=0,
        max=500,
        step=10,
        value=[0, 50],  # Default to shallow depth
        marks={
            0: '0m',
            50: '50m',
            200: '200m',
            500: '500m'
        },
        tooltip={"placement": "bottom", "always_visible": True}
    ),
])
@app.callback(
    output('your-graph-id', 'figure'),
    input('depth-slider', 'value')
)
def update_figure(depth_range):
    # Filter data based on depth range
    filtered_df = df[(df['depth'] >= depth_range[0]) & (df['depth'] <= depth_range[1])]
    
    # Create your figure with filtered data
    fig = px.scatter(filtered_df, x='longitude', y='latitude')
    return fig

# Row 1: Filters and Visualizations
row_one = dbc.Row(
    [
        dbc.Col(
            html.Div([
                html.H4("Filters"),
                chart_selector,
                species_selector,
                depth_slider
            ], className="p-3 bg-light border"),
            width=4
        ),
        dbc.Col(
            html.Div([
                html.H4("Visualizations"),
                html.Div(id="chart-display", children="Chart will render here...")
            ], className="p-3 border"),
            width=8
        ),
    ],
    className="mb-4"
)

# Row 2: Full width for research questions or data logging
row_two = dbc.Row(
    [
        dbc.Col(
            html.Div([
                html.H5("Research Insights"),
                html.P("This section tracks the Global Asteroidea Occurrence Data "
                       "as specified in the NHM dataset (Carter et al., 2025).")
            ], className="p-3 bg-info text-white"),
            width=12
        ),
    ]
)

# Add an HTML layout to the Dash app, for Bootstrap you place the layout in a container
# Wrap the layout in a Bootstrap container
app.layout = dbc.Container(
    children=[
        html.H1("Starfish Data & Tracking app"),
        navbar,
        row_one,
        row_two,
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run(debug=True)
