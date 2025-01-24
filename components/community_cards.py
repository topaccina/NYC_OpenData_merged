from dash import Dash, html
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv("./data/NYC_housingOnly_v0.csv")
df["Borough_CommBoard"] = df["Borough_CommBoard"].str.replace(
    "STATEN IS", "STATEN ISLAND"
)
df["Borough"] = df["Borough"].str.replace("STATEN IS", "STATEN ISLAND")
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

df_EnergyScoreTop["Borough_CommBoard"] = (
    df_EnergyScoreTop.Borough
    + "_"
    + df_EnergyScoreTop["Community Board"].astype(int).astype(str)
)
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
print(df_EnergyScoreTopBor)

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
                    dbc.CardHeader([html.H6(f"{amount[2]}"), html.H2(title)]),
                    dbc.CardBody(html.H5(f"Average: {amount[0]}", id=title)),
                    dbc.CardFooter(html.H6(f"{amount[1]}% with Score over 75")),
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
    borAvg = df_EnergyScoreBorough[
        df_EnergyScoreBorough["Borough"].str.lower() == borSelected.lower()
    ]["ENERGY STAR Score"].values[0]
    NYCTop_pct = 100 * (
        df["ENERGY STAR Score Pass"].sum() / df["ENERGY STAR Score Pass"].count()
    )

    cbTop_pct = df_EnergyScoreTop[
        df_EnergyScoreTop["Borough_CommBoard"].str.lower() == value1.lower()
    ]["ENERGY STAR Score Pass pct"].values[0]
    borTop_pct = df_EnergyScoreTopBor[
        df_EnergyScoreTopBor["Borough"].str.lower() == borSelected.lower()
    ]["ENERGY STAR Score Pass pct"].values[0]
    print("cb")
    print(df_EnergyScoreTop)
    print(df_EnergyScoreBorough)
    print(borTop_pct)
    summary = {
        str(cbIndex): (str(cbAvg.round(1)), str(cbTop_pct.round(1)), "Community Board"),
        str(borSelected): (str(borAvg.round(1)), str(borTop_pct.round(1)), "Borough"),
        "NYC": (str(NYCAvg.round(1)), str(NYCTop_pct.round(1)), "Overall"),
    }

    return [(make_card(k, v)) for k, v in summary.items()]


# summary = {"201": "x", "Bronks": "x", "NYC": "y"}
