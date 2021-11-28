# import dash IO and graph objects
from dash.dependencies import Input, Output

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
#  html, bootstrap components, and tables for datatables
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import State
from datetime import datetime
# import dash_core_components as dcc
# import dash_table

# Import app
from app import app
import pandas as pd
import pathlib as pl
import plotly.express as px
import json


# Import custom data.py
import data as d

PATH = pl.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

df = pd.read_csv(DATA_PATH.joinpath("accidents_2017.csv"))
df = d.praprocess(df)

data = pd.read_csv(DATA_PATH.joinpath("new_accidents_2017.csv"))
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)
df_mild = pd.read_csv(DATA_PATH.joinpath("sum_mild_injuries.csv"))

with open('districtes.geojson') as json_data:
    Barcelona_data = json.load(json_data)

@app.callback(Output('my-graph', 'figure'), 
            inputs=[Input('district','value'),
                    Input('filter-month', 'value')])
def update_graph(district, selected_dropdown_value):
    df_trend = d.trend_month(df, district, selected_dropdown_value)
    if (selected_dropdown_value=='All'):
        data = r_trend_year(df_trend)
    else:
        data = r_trend_month(df_trend)
    
    return data

def r_trend_year(df_):
    return {
        'data': [go.Scatter(
            x=df_['Month'],
            y=df_['total_injuries'],
            mode='lines+markers',
        )]
        # 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}
        
    }

def r_trend_month(df_):
    return {
        'data': [go.Scatter(
            x=df_['Day'],
            y=df_['total_injuries'],
            mode='lines+markers'
        )]
        # 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}
        
    }

@app.callback(
    output=[Output("plot-mild","figure"), 
    Output("plot-serious","figure"),
    Output("output-panel","children")], 

    inputs=[Input("district","value"), 
    Input("date-range","start_date"), 
    Input("date-range","end_date")]
) 
def plot_mild_cases(district, start_date, end_date):
    if district == 'All District':
        df_filter = data.loc[((data['Date'] >= start_date) & (data['Date'] <= end_date))]
        #Mild
        accident_cnt_per_district_mild = df_filter.groupby(by="District_Name").sum()[["Mild_injuries", "Victims", "Vehicles_involved"]]\
                                .rename(columns={"Mild_injuries":"Count_Mild_injuries"})
        accident_avg_lat_lon = df_filter.groupby(by="District_Name").mean()[["Longitude", "Latitude"]]

        accident_cnt_per_district_mild = accident_cnt_per_district_mild.join(accident_avg_lat_lon)
        accident_cnt_per_district_mild = accident_cnt_per_district_mild.reset_index()

        ## mild plots
        fig1 = px.choropleth_mapbox(accident_cnt_per_district_mild, 
                            geojson=Barcelona_data, 
                            color="Count_Mild_injuries",
                            locations="District_Name", 
                            featureidkey="properties.NOM",
                            center={"lat": 41.389223, "lon": 2.167939},
                            mapbox_style="open-street-map", 
                            color_continuous_scale='sunsetdark',
                            zoom=10) 
        fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})   

        #Serious
        accident_cnt_per_district_serious = df_filter.groupby(by="District_Name").sum()[["Serious_injuries", "Victims", "Vehicles_involved"]]\
                                    .rename(columns={"Serious_injuries":"Count_Serious_injuries"})
        accident_avg_lat_lon = df_filter.groupby(by="District_Name").mean()[["Longitude", "Latitude"]]

        accident_cnt_per_district_serious = accident_cnt_per_district_serious.join(accident_avg_lat_lon)
        accident_cnt_per_district_serious = accident_cnt_per_district_serious.reset_index()

        ## main plots
        fig2 = px.choropleth_mapbox(accident_cnt_per_district_serious, 
                            geojson=Barcelona_data, 
                            color="Count_Serious_injuries",
                            locations="District_Name", 
                            featureidkey="properties.NOM",
                            center={"lat": 41.389223, "lon": 2.167939},
                            mapbox_style="open-street-map", 
                            color_continuous_scale='sunsetdark',
                            zoom=10)
        ## set background color
        fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        panel = html.Div([
            html.H4(district),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                
                html.H6("Total Victims:", style={"color":"white"}),
                html.H3("{:,.0f}".format(accident_cnt_per_district_mild['Victims'].sum()), style={"color":"white"}),
                
                html.H6("Total Vehicles Involved:", className="text-danger"),
                html.H3("{:,.0f}".format(accident_cnt_per_district_mild['Vehicles_involved'].sum()), className="text-danger")
            ])
        ])
    else:
        df_filter = data.loc[(data['District_Name'] == district) & ((data['Date'] >= start_date) & (data['Date'] <= end_date))]

        #Mild
        accident_cnt_per_district_mild = df_filter.groupby(by="District_Name").sum()[["Mild_injuries", "Victims", "Vehicles_involved"]]\
                                .rename(columns={"Mild_injuries":"Count_Mild_injuries"})
        accident_avg_lat_lon = df_filter.groupby(by="District_Name").mean()[["Longitude", "Latitude"]]

        accident_cnt_per_district_mild = accident_cnt_per_district_mild.join(accident_avg_lat_lon)
        accident_cnt_per_district_mild = accident_cnt_per_district_mild.reset_index()

        ## mild plots
        fig1 = px.choropleth_mapbox(accident_cnt_per_district_mild, 
                            geojson=Barcelona_data, 
                            color="Count_Mild_injuries",
                            locations="District_Name", 
                            featureidkey="properties.NOM",
                            center={"lat": 41.389223, "lon": 2.167939},
                            mapbox_style="open-street-map", 
                            color_continuous_scale='sunsetdark',
                            zoom=10) 
        fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})   

        #Serious
        accident_cnt_per_district_serious = df_filter.groupby(by="District_Name").sum()[["Serious_injuries", "Victims", "Vehicles_involved"]]\
                                    .rename(columns={"Serious_injuries":"Count_Serious_injuries"})
        accident_avg_lat_lon = df_filter.groupby(by="District_Name").mean()[["Longitude", "Latitude"]]

        accident_cnt_per_district_serious = accident_cnt_per_district_serious.join(accident_avg_lat_lon)
        accident_cnt_per_district_serious = accident_cnt_per_district_serious.reset_index()

        ## main plots
        fig2 = px.choropleth_mapbox(accident_cnt_per_district_serious, 
                            geojson=Barcelona_data, 
                            color="Count_Serious_injuries",
                            locations="District_Name", 
                            featureidkey="properties.NOM",
                            center={"lat": 41.389223, "lon": 2.167939},
                            mapbox_style="open-street-map", 
                            color_continuous_scale='sunsetdark',
                            zoom=10)
        ## set background color
        fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        panel = html.Div([
            html.H4(district),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                
                html.H6("Total Victims:", style={"color":"white"}),
                html.H3("{:,.0f}".format(accident_cnt_per_district_mild['Victims'].sum()), style={"color":"white"}),

                html.H6("Total Vehicles Involved:", className="text-danger"),
                html.H3("{:,.0f}".format(accident_cnt_per_district_mild['Vehicles_involved'].sum()), className="text-danger")
            ])
        ])
        
    return fig1, fig2, panel

@app.callback(
    Output('my_graph1', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value')])
    # State('my_date_picker', 'start_date'),
    # State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker):
    # start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    # end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    
    dfNew = df[df['District Name'] == stock_ticker]
    dff = dfNew.groupby('Neighborhood Name', as_index=False)[['Mild injuries','Serious injuries']].sum()
    
    trace1 = go.Bar(
                y=dff['Neighborhood Name'],  
                x=dff['Mild injuries'],
                orientation='h',
                name = 'Mild Injury',
                marker=dict(color='#FFD700'))

    trace2 = go.Bar(
                y=dff['Neighborhood Name'],
                x=dff['Serious injuries'],
                orientation='h',
                name='Serious Injury',
                marker=dict(color='Crimson'))
    data = [trace1, trace2]
    
    fig = {
        'data': data,
        'layout': go.Layout(
                title='Accident Record in '+stock_ticker,
                barmode='stack'
        )
    }

    return fig
