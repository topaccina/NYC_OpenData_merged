import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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


def cbStar_chart(value1):
    x = df_EnergyScore["Community Board"].astype(int).values
    y = df_EnergyScore["ENERGY STAR Score"].values
    cbIndex = df_info[df_info["Borough_CommBoard"] == value1][
        "Community Board 1"
    ].values[0]
    indexSelected = x.tolist().index(cbIndex)
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
    return fig_star


def cbStar_chart_pct(value1):
    x = df_EnergyScoreTop["Community Board"].astype(int).values
    y = df_EnergyScoreTop["ENERGY STAR Score Pass pct"].values
    cbIndex = df_info[df_info["Borough_CommBoard"] == value1][
        "Community Board 1"
    ].values[0]
    indexSelected = x.tolist().index(cbIndex)
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
        title_text="Pct ENERGY STAR Score over 75 - Community Boards Comparison"
    )
    fig_star.add_hline(
        y=y.mean(),
        line_width=3,
        line_dash="dash",
        line_color="green",
        annotation_text="mean",
        annotation_position="top left",
    )
    return fig_star
