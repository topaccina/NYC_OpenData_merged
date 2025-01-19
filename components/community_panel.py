import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.community_panel_filter import community_panel_filter
from components.community_cards import card_collection
from components.community_info import communityBoard_map_card
from components.community_fig import cbStar_chart, cbStar_chart_pct

#
df = pd.read_csv("./data/NYC_housingOnly_v0.csv")
df_EnergyScore = (
    df[df["Calendar Year"] == 2023]
    .groupby(by=["Borough", "Community Board"])["ENERGY STAR Score"]
    .mean()
    .round(1)
    .reset_index()
)

df["ENERGY STAR Score Pass"] = df[df["Calendar Year"] == 2023][
    "ENERGY STAR Score"
].apply(lambda x: 1 if x >= 75 else 0)
df_EnergyScoreTop = (
    df[df["Calendar Year"] == 2023]
    .groupby(by=["Borough", "Community Board"])
    .aggregate({"ENERGY STAR Score": "count", "ENERGY STAR Score Pass": "sum"})
    .reset_index()
)
df_EnergyScoreTop["ENERGY STAR Score Pass pct"] = (
    df_EnergyScoreTop["ENERGY STAR Score Pass"] / df_EnergyScoreTop["ENERGY STAR Score"]
).round(2) * 100


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

community_card = dbc.Card()
fig_star = go.Figure()
fig_star_pct = go.Figure()
card_summary = {"201": "x", "Bronks": "x", "NYC": "y"}

community_panel = dbc.Container(
    [
        dbc.Row(community_panel_filter),
        dbc.Row([community_card], id="cb_card_map"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            dbc.Row(
                                "",  # card_collection(card_summary),
                                className="my-4",
                                id="cbCard-id",
                            ),
                        )
                    ],
                )
            ],
            className="my-4",
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=fig_star, id="graphStar-id")], md=6, xs=12),
                dbc.Col(
                    [dcc.Graph(figure=fig_star_pct, id="graphStarPct-id")], md=6, xs=12
                ),
            ]
        ),
    ]
)


@callback(
    # Output("graphBorCb-id", "figure"),
    # Output("headerCb-id", "children"),
    # Output("parNbh-id", "children"),
    # Output("parZip-id", "children"),
    Output("cb_card_map", "children"),
    Output("graphStar-id", "figure"),
    Output("graphStarPct-id", "figure"),
    Output("cbCard-id", "children"),
    Input("ddBorCb-id", "value"),
    # prevent_initial_call=True,
)
def update_dropdown_options(value1):

    fig_star = cbStar_chart(value1)
    fig_star_pct = cbStar_chart_pct(value1)

    cbCard = card_collection(value1)
    cb_card_map = communityBoard_map_card(value1)

    return cb_card_map, fig_star, fig_star_pct, cbCard
