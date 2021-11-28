# import dash-core, dash-html, dash io, bootstrap
import os

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks
from navbar import Navbar
import layout as l

import callbacks

# Import app
from app import app

# Import server for deployment
from app import srv as server

from settings import config


app_name = os.getenv("DASH_APP_PATH", "/accidents-viz")

# Layout variables, navbar, header, content, and container
nav = Navbar()

header = dbc.Row(
    dbc.Col(
        html.Div(
            [
                html.Br(),
                html.H1(children=config.name, id="nav-pills"),
                nav,
                html.Br(),html.Br(),html.Br(),
            ]
        )
    ),
    className="banner",
)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

container = dbc.Container(fluid=True, children=[content])


# Menu callback, set and return
# Declair function  that connects other pages with content to container
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname.endswith("/series"):
        return l.seriesLayout
    elif pathname.endswith("/spatial"):
        return l.spatialLayout
    elif pathname.endswith("/categorical"):
        return l.categoricalLayout    
    else:
        return l.spatialLayout


# Main index function that will call and return all layout variables
def index():
    layout = html.Div([header, container])
    return layout


# Set layout to index function
app.layout = index()

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True)
