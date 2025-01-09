import dash_bootstrap_components as dbc
from dash import html, dcc, callback, callback_context, Input, Output, no_update
import pandas as pd

df = pd.read_csv("./data/NYC_housingOnly_v0.csv")


df_info = pd.read_csv(
    "./data/NYC_Community_Boards.csv",
    usecols=[
        "Borough",
        "Community Board",
        "Neighborhoods",
        "Latitude",
        "Longitude",
        "Community Board 1",
        "Postcode",
        "Location Point",
    ],
)
df_info["Borough_CommBoard"] = (
    df_info.Borough + "_" + df_info["Community Board 1"].astype(str)
)
ddBorCb = dcc.Dropdown(
    options=df_info["Borough_CommBoard"].unique().tolist(),
    value=df_info["Borough_CommBoard"].tolist()[0],
    id="ddBorCb-id",
    clearable=False,
)


community_panel_filter = dbc.Card(
    [
        # dbc.CardHeader(),
        dbc.CardBody(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [ddBorCb],
                                    width=4,
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
    ],
    className="mt-1 mb-2",
)
