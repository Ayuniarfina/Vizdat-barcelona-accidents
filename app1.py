import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.graph_objs as go

import os
import pathlib as pl
import pandas as pd
import numpy as np
import plotly.express as px
# from pandas_datareader import data as web
from datetime import datetime as dt

import utils

app = dash.Dash('Hello World')


APP_PATH = str(pl.Path(__file__).parent.resolve())

df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "accidents_2017.csv")))
df = utils.praprocess(df)

# fig = px.line(df_year, x="Month", y=['Mild injuries', 'Serious injuries', 'Victims'])

indicators_month = df['Month'].unique()
indicators_month = np.append(indicators_month, 'All')

app.layout = html.Div([
    dcc.Dropdown(
                id='filter-month',
                options=[{'label': i, 'value': i} for i in indicators_month],
                value='All'
            ), 
    dcc.Graph(
        id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('filter-month', 'value')])
def update_graph(selected_dropdown_value):
    df_trend = utils.trend_month(df, selected_dropdown_value)
    if (selected_dropdown_value=='All'):
        data = r_trend_year(df_trend)
    else:
        data = r_trend_month(df_trend)
    
    return data


def r_trend_year(data):
    return {
        'data': [go.Scatter(
            x=data['Month'],
            y=data['total_injuries'],
            mode='lines+markers'
        )]
        # 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}
        
    }

def r_trend_month(data):
    return {
        'data': [go.Scatter(
            x=data['Day'],
            y=data['total_injuries'],
            mode='lines+markers'
        )]
        # 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}
        
    }

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()
