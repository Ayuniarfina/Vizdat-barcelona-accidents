import pandas as pd
import numpy as np
import pathlib as pl
import plotly.express as px
import json
import plotly.graph_objects as go

# Dash components, html, and dash tables
from dash import dcc
from dash import html
from dash import dash_table

# Import Bootstrap components
import dash_bootstrap_components as dbc

# Import custom data.py
import data

PATH = pl.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

df = pd.read_csv(DATA_PATH.joinpath("accidents_2017.csv"))
df = data.praprocess(df)

# fig = px.line(df_year, x="Month", y=['Mild injuries', 'Serious injuries', 'Victims'])

indicators_month = df['Month'].unique()
indicators_month = np.append(indicators_month, 'All')

df.sort_values("Date", inplace=True)

df_mild = pd.read_csv(DATA_PATH.joinpath("sum_mild_injuries.csv"))
with open('districtes.geojson') as json_data:
    Barcelona_data = json.load(json_data)

# mapbox token
mapbox_accesstoken = 'pk.eyJ1Ijoiam9zdWFjcmlzaGFuIiwiYSI6ImNrdnFmcDlsaTRobzMyd255YjZ1OHNycnUifQ.BWZNmYH2Z-iNl1beZathAQ'

fig1 = go.Figure(go.Scattermapbox(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5
        ),
        text=df['District Name'],
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

# Input
inputs_district = dbc.Form([
    html.H4("Select District"),
    dcc.Dropdown(id="district", options=[{"label":x,"value":x} for x in np.insert(df_mild.District_Name.unique(), 0, "All District")], value="All District")
]) 

inputs_months = dbc.Form([
    html.H4("Select Month"),
    dcc.Dropdown(id="filter-month", options=[{'label': i, 'value': i} for i in indicators_month], value="All")
]) 

inputs_date = dbc.Form([
    html.H4("Select Range Date"),
    dcc.DatePickerRange(
        id="date-range",
        min_date_allowed=df.Date.min().date(),
        max_date_allowed=df.Date.max().date(),
        start_date=df.Date.min().date(),
        end_date=df.Date.max().date(),
    )
]) 

seriesLayout = html.Div([
    dbc.Row([
        dbc.Col(md=3, children=[
            inputs_district, 
            html.Br(),

            inputs_months,
            # html.Br(),html.Br()
        ]),

        dbc.Col(md=9, children=[
            dcc.Graph(id='my-graph')
        ])
    ])
],
className="app-page",
) 

spatialLayout = html.Div([ 
    dbc.Row([
            ### input + panel
            dbc.Col(md=3, children=[
                inputs_district, 
                html.Br(),

                inputs_date,
                html.Br(),html.Br(),
                
                html.Div(id="output-panel")
            ]),
            ### plots
            dbc.Col(md=9, children=[
                # dbc.Col(html.H4("Barcelona Accidents"), width={"size":6,"offset":3}), 
                dbc.Tabs(className="nav nav-pills", children=[
                    dbc.Tab(dcc.Graph(id="plot-mild"), label="Mild injuries"),
                    dbc.Tab(dcc.Graph(id="plot-serious"), label="Serious injuries")
                ])
            ])
        ])
    ], 
    className="app-page",
)


