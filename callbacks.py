# import dash IO and graph objects
from dash.dependencies import Input, Output

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import dash html, bootstrap components, and tables for datatables
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_table

# Import app
from app import app
import pandas as pd
import pathlib as pl


# Import custom data.py
import data as d

PATH = pl.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

df = pd.read_csv(DATA_PATH.joinpath("accidents_2017.csv"))
df = d.praprocess(df)

@app.callback(Output('my-graph', 'figure'), [Input('filter-month', 'value')])
def update_graph(selected_dropdown_value):
    df_trend = d.trend_month(df, selected_dropdown_value)
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
            mode='lines+markers'
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