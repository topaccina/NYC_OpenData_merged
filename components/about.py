from dash import Dash, html
import dash_bootstrap_components as dbc
import pandas as pd


about_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div(
                    [
                        """Local Law 84 of 2009 (LL84) requires annual energy 
                                   and water benchmarking data to be submitted by owners of buildings with more than 50,000 square feet."""
                    ]
                ),
                html.Div(
                    [
                        """This data is collected via the Environmental Protection Agency (EPA) Portfolio Manager website"""
                    ]
                ),
                html.Div(
                    [
                        """    A very comphensive snapshot of buildings energy performance."""
                    ]
                ),
                html.Div(
                    [
                        """"What do you know about.. your city, your neighboorhoods, your house?"""
                    ]
                ),
                html.Div(["""Learn from NYC Open data..."""]),
            ]
        )
    ]
)

about_panel = dbc.Container([dbc.Row([dbc.Col([about_card])])])
