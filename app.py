# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os

import pathlib as pl
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

import utils

app = dash.Dash()
app.title = "Barcelona Accidents"
server = app.server

# colors = {
#     'background': '#EEEEEE',
#     'text': '#181D31'
# }

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


APP_PATH = str(pl.Path(__file__).parent.resolve())

df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "accidents_2017.csv")))
df = utils.praprocess(df)
df_year = utils.trend_year(df)

fig = px.line(df, x="Month", y=['Mild injuries', 'Serious injuries', 'Victims'])
indicators_month = df_year['Month'].unique()
indicators_day = df['Day'].unique()

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='filter-month',
                options=[{'label': i, 'value': i} for i in indicators_month],
                value='All'
            )
        ],
        style={'width':'48%', 'display':'inline-block'}),

        html.Div([ 
            dcc.Dropdown(
                id='filter-day',
                options=[{'label': i, 'value': i} for i in indicators_day],
                value='All'
            )
        ],
        style={'width':'48%', 'display':'inline-block'})
    ],
    style= {
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([ 
        dcc.Graph(id='trend-year'
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([ 
        dcc.Graph(id='trend-month'),
        dcc.Graph(id='trend-day'),
    ], style={'display': 'inline-block', 'width': '48%'})
])

@app.callback(
    dash.dependencies.Output('trend-year', 'figure'),
    [dash.dependencies.Input('filter-month', 'value'),
    dash.dependencies.Input('filter-day', 'value')]
)

def update_graph(months, days):
    df_month = utils.trend_month(df, months)
    df_day = utils.trend_day(df, months, days)
    return {
        'data': [go.scatter(
            x=df_year['Month'],
            y=df_year[['Mild injuries', 'Seriouos injuries', 'Victims']],
            mode='lines+markers'
        )],
        'layout': go.layout(
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
