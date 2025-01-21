from dash import Dash, html
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv("./data/NYC_housingOnly_v0.csv")
df_EnergyScore = (
    df[df["Calendar Year"] == 2023]
    .groupby(by=["Borough", "Community Board"])["ENERGY STAR Score"]
    .mean()
    .round(1)
    .reset_index()
)
df_EnergyScoreBorough = (
    df[df["Calendar Year"] == 2023]
    .groupby(by=["Borough"])["ENERGY STAR Score"]
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


#######################
df_EnergyScoreTopBor = (
    df[df["Calendar Year"] == 2023]
    .groupby(by=["Borough"])
    .aggregate({"ENERGY STAR Score": "count", "ENERGY STAR Score Pass": "sum"})
    .reset_index()
)
df_EnergyScoreTopBor["ENERGY STAR Score Pass pct"] = (
    df_EnergyScoreTopBor["ENERGY STAR Score Pass"]
    / df_EnergyScoreTopBor["ENERGY STAR Score"]
).round(2) * 100
#########################################


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


def make_card(title, amount):
    return dbc.Col(
        [
            dbc.Card(
                [
                    dbc.CardHeader(html.H2(title)),
                    dbc.CardBody(html.H5(f"Average: {amount}", id=title)),
                    dbc.CardFooter(html.H6(f"{amount}% with Score over 75")),
                ],
                className="text-center shadow",
            )
        ]
    )


def card_collection(value1):
    x = df_EnergyScore["Community Board"].astype(int).values
    y = df_EnergyScore["ENERGY STAR Score"].values
    cbIndex = df_info[df_info["Borough_CommBoard"] == value1][
        "Community Board 1"
    ].values[0]
    indexSelected = x.tolist().index(cbIndex)
    cbAvg = y[indexSelected]
    borSelected = df_info[df_info["Borough_CommBoard"] == value1]["Borough"].values[0]
    NYCAvg = df_EnergyScore["ENERGY STAR Score"].mean()
    cbTop_pct = ""
    summary = {
        str(value1): str(cbAvg),
        str(borSelected): "x",
        "NYC": str(NYCAvg.round(1)),
    }

    return [(make_card(k, v)) for k, v in summary.items()]


# summary = {"201": "x", "Bronks": "x", "NYC": "y"}
