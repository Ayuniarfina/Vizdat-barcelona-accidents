import os
import pathlib as pl
import json
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import json
import numpy as np
from dash.dependencies import Output, Input
from settings import config
# from python.data import Data
# from python.model import Model
# from python.result import Result

import utils

APP_PATH = str(pl.Path(__file__).parent.resolve())

data = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "accidents_2017.csv")))
data = utils.praprocess(data)
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)
df_mild = pd.read_csv("sum_mild_injuries.csv")
df_serious = pd.read_csv("sum_serious_injuries.csv")

with open('districtes.geojson') as json_data:
    Barcelona_data = json.load(json_data)

# mapbox token
mapbox_accesstoken = 'pk.eyJ1Ijoiam9zdWFjcmlzaGFuIiwiYSI6ImNrdnFmcDlsaTRobzMyd255YjZ1OHNycnUifQ.BWZNmYH2Z-iNl1beZathAQ'

fig1 = go.Figure(go.Scattermapbox(
        lat=data['Latitude'],
        lon=data['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5
        ),
        text=data['District Name'],
    ))

fig1.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_accesstoken,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=41.389223,
            lon=2.167939
        ),
        pitch=0,
        zoom=11
    ),
    margin={"r":0,"t":0,"l":0,"b":0}
)

fig2 = px.choropleth_mapbox(df_mild, 
                            geojson=Barcelona_data, 
                            color="Count_Mild_injuries",
                            locations="District_Name", 
                            featureidkey="properties.NOM",
                            center={"lat": 41.389223, "lon": 2.167939},
                            mapbox_style="open-street-map", 
                            zoom=10)

fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig3 = px.choropleth_mapbox(df_serious, 
                            geojson=Barcelona_data, 
                            color="Count_Serious_injuries",
                            locations="District_Name", 
                            featureidkey="properties.NOM",
                            center={"lat": 41.389223, "lon": 2.167939},
                            mapbox_style="open-street-map", 
                            zoom=10)

fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app = dash.Dash(name=config.name, assets_folder=config.root+"/assets", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.name

# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## logo/home
    dbc.NavItem(html.Img(src=app.get_asset_url("/static/logo.PNG"), height="40px")),
    ## Categorical
    dbc.NavItem(html.Div([
        dbc.NavLink("Categorical", href="/", active=False)
        # ,
        # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
        #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
        # ])
    ])),
    ## Temporal
    dbc.NavItem(html.Div([
        dbc.NavLink("Temporal", href="/", active=False)
        # ,
        # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
        #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
        # ])
    ])),
    ## Spatial
    dbc.NavItem(html.Div([
        dbc.NavLink("Spatial", href="/#", active=False)
        # ,
        # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
        #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
        # ])
    ])),
    ## Hierarchical
    dbc.NavItem(html.Div([
        dbc.NavLink("Hierarchical", href="/", active=False)
        # ,
        # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
        #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
        # ])
    ])),
    ## about
    dbc.NavItem(html.Div([
        dbc.NavLink("About", href="/", active=False)
        # ,
        # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
        #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
        # ])
    ])),
    ## links
    dbc.DropdownMenu(label="Links", nav=True, children=[
        dbc.DropdownMenuItem([html.I(className="fa fa-database"), "  Data Sources"], href=config.contacts, target="_blank"), 
        dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href=config.code, target="_blank"),
        dbc.DropdownMenuItem([html.I(className="fa fa-google"), "  Google Form"], href=config.google_form, target="_blank")
    ])
])

# Input
inputs_district = dbc.Form([
    html.H4("Select District"),
    dcc.Dropdown(id="district", options=[{"label":x,"value":x} for x in np.insert(df_mild.District_Name.unique(), 0, "All District")], value="All District")
]) 
inputs_date = dbc.Form([
    html.H4("Select Range Date"),
    dcc.DatePickerRange(
        id="date-range",
        min_date_allowed=data.Date.min().date(),
        max_date_allowed=data.Date.max().date(),
        start_date=data.Date.min().date(),
        end_date=data.Date.max().date(),
    )
]) 

# App Layout
app.layout = dbc.Container(fluid=True, children=[
    # html.P(print(df_mild.District_Name.unique())),
    ## Top
    html.Br(),
    html.H1(config.name, id="nav-pills"),
    navbar,
    html.Br(),html.Br(),html.Br(),

    ## Body
    dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
            inputs_district, 
            html.Br(),

            inputs_date,
            html.Br(),html.Br(),html.Br(),
            
            html.Div(id="output-panel")
        ]),
        ### plots
        dbc.Col(md=9, children=[
            # dbc.Col(html.H4("Barcelona Accidents"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="plot-mild", figure=fig2), label="Mild injuries"),
                dbc.Tab(dcc.Graph(id="plot-serious", figure=fig3), label="Serious injuries")
            ])
        ])
    ])
])

# Python function to plot Mild cases
# @app.callback(output=Output("plot-mild","figure"), inputs=[Input("district","value")]) 
# def plot_mild_cases(district):
#     data.process_data(district) 
#     model = Model(data.dtf)
#     result = Result(model.dtf)
#     return result.plot_mild(model.today)

# # Python function to plot serious cases
# @app.callback(output=Output("plot-serious","figure"), inputs=[Input("district","value")])
# def plot_serious_cases(district):
#     data.process_data(district) 
#     model = Model(data.dtf)
#     result = Result(model.dtf)
#     return result.plot_serious(model.today)

# # Python function to render output panel
# @app.callback(output=Output("output-panel","children"), inputs=[Input("district","value")])
# def render_output_panel(district):
#     data.process_data(district) 
#     model = Model(data.dtf)
#     result = Result(model.dtf)
#     peak_day, num_max, total_cases_until_today, total_cases_in_30days, active_cases_today, active_cases_in_30days = result.get_panel()
#     peak_color = "white" if model.today > peak_day else "red"
#     panel = html.Div([
#         html.H4(district),
#         dbc.Card(body=True, className="text-white bg-primary", children=[
            
#             html.H6("Total cases until today:", style={"color":"white"}),
#             html.H3("{:,.0f}".format(total_cases_until_today), style={"color":"white"}),
            
#             html.H6("Total cases in 30 days:", className="text-danger"),
#             html.H3("{:,.0f}".format(total_cases_in_30days), className="text-danger"),
            
#             html.H6("Active cases today:", style={"color":"white"}),
#             html.H3("{:,.0f}".format(active_cases_today), style={"color":"white"}),
            
#             html.H6("Active cases in 30 days:", className="text-danger"),
#             html.H3("{:,.0f}".format(active_cases_in_30days), className="text-danger"),
            
#             html.H6("Peak day:", style={"color":peak_color}),
#             html.H3(peak_day.strftime("%Y-%m-%d"), style={"color":peak_color}),
#             html.H6("with {:,.0f} cases".format(num_max), style={"color":peak_color})
        
#         ])
#     ])
#     return panel
# 
# @app.callback(
#     [Output("price-chart", "figure"), Output("volume-chart", "figure")],
#     [
#         Input("Part_of_the_day-filter", "value"),
#         Input("Injuries-filter", "value"),
#         Input("date-range", "start_date"),
#         Input("date-range", "end_date"),
#     ],
# )

if __name__ == "__main__":
    app.run_server(debug=True)