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
from datetime import datetime

# Import Bootstrap components
import dash_bootstrap_components as dbc

# Import custom data.py
import data

PATH = pl.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

df = pd.read_csv(DATA_PATH.joinpath("accidents_2017.csv"))
df = data.praprocess(df)
dfBar = pd.read_csv(DATA_PATH.joinpath("new_accidents_2017.csv"))

# fig = px.line(df_year, x="Month", y=['Mild injuries', 'Serious injuries', 'Victims'])

indicators_month = df['Month'].unique()
indicators_month = np.append(indicators_month, 'All')

df.sort_values("Date", inplace=True)

df_mild = pd.read_csv(DATA_PATH.joinpath("sum_mild_injuries.csv"))
with open('districtes.geojson') as json_data:
    Barcelona_data = json.load(json_data)
    
accident_df=df
accident_df['killed+injured'] = df['Mild injuries'] + df['Serious injuries'] + df['Victims']
temp_df = accident_df.groupby(['District Name'])['killed+injured'].sum().sort_values(axis=0, ascending=False)


trace0 = go.Bar(x = temp_df.index,
                y = temp_df.values,
                marker = dict(color=list(temp_df.values))
                )

data = [trace0]


wkday = accident_df.groupby(['Weekday']).\
        agg({'Mild injuries':'sum', 'Serious injuries':'sum'}).reset_index()
wkday

ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
      "Sunday"]

# sorting data accoring to ordered_days
wkday['to_sort']=wkday['Weekday'].apply(lambda x:ordered_days.index(x))
wkday1 = wkday.sort_values('to_sort')

trace01 = go.Bar(x = wkday1['Weekday'],
                y= wkday1['Mild injuries'],
                name = "Mild injuries",
                marker = dict(color='rgb(108, 52, 131)')
               )

trace11 = go.Bar(x = wkday1['Weekday'],
                y = wkday1['Serious injuries'],
                name = "Serious injuries",
                marker = dict(color='rgb(241, 196, 15)')
               )


data1 = [trace01,trace11]

dff = dfBar.groupby('District_Name', as_index=False)[['Mild_injuries','Serious_injuries']].sum()

options1 = ["All District"]
for tic in dfBar['District_Name'].unique():
    options1.append(tic)
	
trace1all = go.Bar(
                y=dff['District_Name'],  
                x=dff['Mild_injuries'],
                orientation='h',
                name = 'Mild Injury',
                marker=dict(
                    color='rgba(50, 171, 96, 0.6)',
                    line=dict(
                        color='rgba(50, 171, 96, 1.0)',
                        width=1),))
trace2all = go.Bar(
                y=dff['District_Name'],
                x=dff['Serious_injuries'],
                orientation='h',
                name='Serious Injury',
                marker=dict(color='Crimson',
                        line=dict(
                            color='Crimson',
                        width=1),))
data_all = [trace1all, trace2all]

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

inputs_district2 = dbc.Form([
                    html.H4("Select District"),
                    dcc.Dropdown(id="my_ticker_symbol",
                    options=[
                        {'label': i, 'value': i} for i in options1],
                    value='All District',
                    multi=False
                )])

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

inputs_date2 = dbc.Form([
                    html.H4("Select Range Date"),
                    dcc.DatePickerRange(
                        id='my_date_picker',
                        min_date_allowed=datetime(2017, 1, 1),
                        max_date_allowed=datetime(2017, 12, 31),
                        start_date=datetime(2017, 1, 1),
                        end_date=datetime(2017, 12, 31)
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

# hierarchicalLayout = html.Div([ 
    # dbc.Row([
            # dbc.Col(md=3, children=[
                # inputs_district, 
                # html.Br(),

                # inputs_date,
                # html.Br(),html.Br(),
                
            # ]),
			# dbc.Col(md=9, children=[
            # dcc.Graph(id='hgraph')
			# ])
        # ])
    # ], 
# className="app-page",
# )
hierarchicalLayout = html.Div([
    dbc.Row([
            dbc.Col(md=3, children=[
                inputs_district2, 
                html.Br(),

                inputs_date2,
                html.Br(),html.Br(),
                
                html.Div([
                    html.Button(
                        id='submit-button',
                        n_clicks=0,
                        children='Submit',
                        # style={'fontSize':24, 'marginLeft':'30px'}
                    ),
                ], #style={'display':'inline-block'}),
                ),
            ]),
			dbc.Col(md=9, children=[
            dcc.Graph(
                id='my_graph1',
                figure={'data': data_all,
                        'layout': go.Layout(
                        title = 'Accident Record based on District',
                        barmode='stack')})
			])
        ])
    ], 
className="app-page",
)


categoricalLayout = html.Div(children=[
    # html.H1(children='Barcelona Accident'),
    html.Div(children=''''''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace0],
            'layout':
            go.Layout(xaxis = dict(tickangle=-30),
                      title='Top Districts Where People Killed and Injured in Accidents', barmode='group',
                      xaxis_title="District",
                   yaxis_title="Victims")
        }),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace01, trace11],
            'layout':
            go.Layout(xaxis = dict(tickangle=-30),
                      title='Weekday-Wise Accidents in Barcelona', barmode='group',
                      xaxis_title="Weekday",
                   yaxis_title="Victims")
        })
    ], 
    className="app-page",
)




