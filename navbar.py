import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import os

from settings import config
from app import app

app_name = os.getenv("DASH_APP_PATH", "/accidents-viz")

def Navbar():
    nav = dbc.Nav(className="nav nav-pills", children=[
        ## logo/home
        dbc.NavItem(html.Img(src=app.get_asset_url("/static/logo.PNG"), height="40px")),
        ## Categorical
        dbc.NavItem(html.Div([
            dbc.NavLink("Categorical", href=f"{app_name}/categorical", className="tab")
            # ,
            # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
            # ])
        ])),
        ## Temporal
        dbc.NavItem(html.Div([
            dbc.NavLink("Temporal", href=f"{app_name}/series")
            # ,
            # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
            # ])
        ])),
        ## Spatial
        dbc.NavItem(html.Div([
            dbc.NavLink("Spatial", href=f"{app_name}/spatial")
            # ,
            # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
            # ])
        ])),
        ## Hierarchical
        dbc.NavItem(html.Div([
            dbc.NavLink("Hierarchical", href=f"{app_name}/hierarchical", active=False)
            # ,
            # dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            #     dbc.PopoverHeader("How it works"), dbc.PopoverBody()
            # ])
        ])),
        ## links
        dbc.DropdownMenu(label="Links", nav=True, children=[
            dbc.DropdownMenuItem([html.I(className="fa fa-database"), "  Data Sources"], href="https://www.kaggle.com/xvivancos/barcelona-data-sets", target="_blank"), 
            dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href="https://github.com/Ayuniarfina/Vizdat-barcelona-accidents", target="_blank"),
            dbc.DropdownMenuItem([html.I(className="fa fa-google"), "  Google Form"], href="https://docs.google.com/forms/d/e/1FAIpQLSefti91PgTJYOIFz2VhJYDAPnWxZBT70MDj27nrmVhAREYVgg/viewform", target="_blank")
        ])
    ])
    return nav
