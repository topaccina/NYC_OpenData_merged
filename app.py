import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import json

# import local components
from components.navbar import navbar
from components.info_table import grid
from components.community_panel import community_panel
from components.city_view import city_panel

#
# read data
# df = pd.read_csv("./data/NYC_housingOnly_v0.csv")
# df = df.astype({"ENERGY STAR Score": float})
# with open("./data/new-york-zip-codes-_1604.geojson") as f:
#     zip_geojson = json.load(f)
# df_cb = df[df.Borough == "QUEENS"].reset_index().drop(columns="index")
#

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

accordion = dbc.Accordion(
    [
        dbc.AccordionItem(
            [city_panel],
            title="Your City ...",
            className="mt-1 ms-2 me-2 primary",
        ),
        dbc.AccordionItem(
            [community_panel],
            title="Your Community ...",
            className="mt-1 ms-2 me-2 primary",
        ),
        dbc.AccordionItem(
            [
                html.P("This is the content of the second section"),
                dbc.Button("Don't click me!", color="danger"),
            ],
            title="Your Building ...",
            className="mt-1 ms-2 me-2",
        ),
    ],
)
tab1_content = dbc.Container(
    [
        # dbc.Card(
        #     dbc.CardBody([filterPanel]),
        #     className="mt-3",
        # ),
        dbc.Card(
            dbc.CardBody([accordion]),
            className="mt-3",
        ),
    ]
)

tab2_content = dbc.Card(
    dbc.CardBody([grid]),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Your Search"),
        dbc.Tab(tab2_content, label="NYC Info"),
        # dbc.Tab("This tab's content is never seen", label="Tab 3", disabled=True),
    ],
)

app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col([navbar])]),
        # dbc.Row([dbc.Col([tabs])]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([tabs], className="mt-3 mb-3"),
                    ],
                    className="m-3",
                    width=12,
                ),
                dbc.Col(
                    [],
                    # width=4,
                ),
            ],
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
