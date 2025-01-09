import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.community_panel_filter import community_panel_filter

#
df = pd.read_csv("./data/NYC_housingOnly_v0.csv")
df_EnergyScore = (
    df.groupby(by=["Borough", "Community Board"])["ENERGY STAR Score"]
    .mean()
    .round(1)
    .reset_index()
)

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
# placeholder (by now ...)
df_cb = df_info[df_info["Borough_CommBoard"] == "Bronx_201"]
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

community_card = dbc.Card(
    [
        dbc.CardHeader(
            ["Bronx_201"], id="headerCb-id", className="bg-primary fw-bold text-light  "
        ),
        dbc.CardBody(
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6("Neighboorhoods", className="card-title"),
                                    html.P(
                                        ["Mott Haven, Port Morris, and Melrose"],
                                        className="card-text",
                                        id="parNbh-id",
                                    ),
                                    html.H6("Zip Code", className="card-title"),
                                    html.P(
                                        ["10455"], className="card-text", id="parZip-id"
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


# x = [cb for cb in df_info["Community Board 1"].astype(int).unique()]
x = df_EnergyScore["Community Board"].astype(int).values
y = df_EnergyScore["ENERGY STAR Score"].values
indexSelected = x.tolist().index(201)
colors = [
    "lightslategray",
] * len(x)
colors[indexSelected] = "crimson"
fig_star = go.Figure(
    data=[
        go.Bar(
            x=x.astype(str),
            y=y,
            marker_color=colors,  # marker color can be a single color value or an iterable
        )
    ]
)
fig_star.update_layout(
    title_text="Average ENERGY STAR Score - Community Boards Comparison"
)
fig_star.add_hline(
    y=y.mean(),
    line_width=3,
    line_dash="dash",
    line_color="green",
    annotation_text="mean",
    annotation_position="top left",
)

community_panel = dbc.Container(
    [
        dbc.Row(community_panel_filter),
        dbc.Row(community_card),
        dbc.Row(dcc.Graph(figure=fig_star)),
    ]
)


@callback(
    Output("graphBorCb-id", "figure"),
    Output("headerCb-id", "children"),
    Output("parNbh-id", "children"),
    Output("parZip-id", "children"),
    Input("ddBorCb-id", "value"),
    # prevent_initial_call=True,
)
def update_dropdown_options(value1):
    df_cb = df_info[df_info["Borough_CommBoard"] == value1]
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

    return fig_cb, headerCb, nbhList, zipCb
