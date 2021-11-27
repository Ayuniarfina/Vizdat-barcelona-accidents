import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from settings import config

app = dash.Dash(
    # __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    name=config.name, assets_folder=config.root+"/assets", external_stylesheets=[dbc.themes.LUX, config.fontawesome]
    )

app.title = config.name
srv = app.server

# set app callback exceptions to true
app.config.suppress_callback_exceptions = True

# app.layout = html.Div(
#     [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
# )