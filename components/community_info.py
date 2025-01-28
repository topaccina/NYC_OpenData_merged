import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

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


def communityBoard_map(borough_commBoard):
    df_cb = df_info[df_info["Borough_CommBoard"] == borough_commBoard]
    fig_cb = px.scatter_map(
        df_cb,
        lat="Latitude",
        lon="Longitude",
        zoom=10,
        text="Borough_CommBoard",
    )

    fig_cb.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_cb.update_layout(map_style="open-street-map")
    fig_cb.update_traces(textposition="top center")

    df_cb = df_info[df_info["Borough_CommBoard"] == borough_commBoard]
    fig_cb = px.scatter_map(
        df_cb,
        lat="Latitude",
        lon="Longitude",
        zoom=10,
        text="Borough_CommBoard",
    )

    fig_cb.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_cb.update_layout(map_style="open-street-map")
    fig_cb.update_traces(textposition="top center")
    nbhList = df_cb["Neighborhoods"].values[0]
    headerCb = df_cb["Borough_CommBoard"].values[0]
    zipCb = df_cb["Postcode"].values[0]
    return fig_cb, nbhList, headerCb, zipCb


# placeholder (by now ...)
# df_cb = df_info[df_info["Borough_CommBoard"] == "Bronx_201"]
# fig_cb = px.scatter_map(
#     df_cb,
#     lat="Latitude",
#     lon="Longitude",
#     zoom=10,
#     text="Borough_CommBoard",
# )

# fig_cb.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig_cb.update_layout(map_style="open-street-map")
# fig_cb.update_traces(textposition="top center")

# fig_cb=communityBoard_map("Bronx_201")


def communityBoard_map_card(borough_commBoard):
    fig_cb, nbhList, headerCb, zipCb = communityBoard_map(borough_commBoard)
    community_card = dbc.Card(
        [
            dbc.CardHeader(
                [headerCb],
                id="headerCb-id",
                style={
                    "backgroundColor": "#006BB6",  # New York blue
                    "color": "white",  # White text
                    "fontWeight": "bold",  # Bold text for emphasis
                    "padding": "10px",  # Padding for spacing
                },
                # className="bg-primary fw-bold text-light mt-2  ",
            ),
            dbc.CardBody(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H6(
                                            "Neighboorhoods", className="card-title"
                                        ),
                                        html.P(
                                            nbhList,
                                            className="card-text",
                                            id="parNbh-id",
                                        ),
                                        html.H6("Zip Code", className="card-title"),
                                        html.P(
                                            [zipCb],
                                            className="card-text",
                                            id="parZip-id",
                                        ),
                                    ],
                                    width=7,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            figure=fig_cb,
                                            id="graphBorCb-id",
                                            style={"height": "20vh"},
                                        )
                                    ],
                                    width=5,
                                ),
                            ]
                        )
                    ]
                )
            ),
        ],
        className=" mb-3",
    )
    return community_card
