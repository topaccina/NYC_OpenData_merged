from dash import Dash, dcc, html, Input, Output, State, callback, no_update
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# data = pd.read_csv(
#     "NYC_Building_Energy_and_Water_Data_Disclosure_for_Local_Law_84__2022-Present__20250104.csv"
# )
# data = data[
#     (data["ENERGY STAR Score"] != "Not Available") & (data["Calendar Year"] == 2023)
# ]

data = pd.read_csv("./data/NYC_housingOnly_v0.csv")
data = data[data["Calendar Year"] == 2023]
# df["Postal Code"] = df["Postal Code"].astype(str)
data_scatter_map = px.scatter_map(
    data,
    lat="Latitude",
    lon="Longitude",
    hover_data=["Address 1", "ENERGY STAR Score"],
    custom_data=["Property ID", "Postal Code"],
    map_style="open-street-map",
    zoom=9,
)


# app = Dash(suppress_callback_exceptions=True)
selBuilding_panel = dbc.Container(
    [
        # dag.AgGrid(
        #     rowData=data.to_dict("records"),
        #     columnDefs=[{"field": i} for i in data.columns],
        #     dashGridOptions={"pagination": True},
        # ),
        dcc.Graph(id="my-graph", figure=data_scatter_map),
        dcc.Dropdown(
            id="my-dropdown",
            options=["Year Built", "ENERGY STAR Score", "Site Energy Use (kBtu)"],
            value="Year Built",
            clearable=False,
        ),
        html.Div(id="figure-space"),
        html.H2(
            "Find and click any building marker on the map",
            style={"textAlign": "center"},
        ),
    ]
)


@callback(
    Output("figure-space", "children"),
    Input("my-graph", "clickData"),
    Input("my-dropdown", "value"),
    prevent_initial_call=True,
)
def more_info(clicked_data, col_selected):
    if clicked_data is None:
        return no_update
    else:
        print(clicked_data)
        clicked_property_id = clicked_data["points"][0]["customdata"][0]
        clicked_zip_code = clicked_data["points"][0]["customdata"][1]
        clicked_energy_score = clicked_data["points"][0]["customdata"][3]

        df_limited = data[data["Postal Code"] == clicked_zip_code]
        df_limited["ENERGY STAR Score"] = pd.to_numeric(
            df_limited["ENERGY STAR Score"], errors="coerce"
        ).astype("Int64")
        df_limited["Site Energy Use (kBtu)"] = pd.to_numeric(
            df_limited["Site Energy Use (kBtu)"], errors="coerce"
        )

        fig = px.scatter(
            df_limited,
            x=col_selected,
            y="ENERGY STAR Score",
            title=f"Visualization for buildings in zip code: {clicked_zip_code}",
        )
        df_limited["color"] = df_limited["Property ID"].apply(
            lambda x: "blue" if x == clicked_property_id else "red"
        )
        fig.update_traces(marker_color=df_limited["color"])
        x_axis_annotation = (
            df_limited[df_limited["Property ID"] == clicked_property_id][col_selected]
            .values[0]
            .item()
        )
        fig.add_annotation(
            x=x_axis_annotation,
            y=clicked_energy_score,
            text="Your clicked building",
            showarrow=False,
            yshift=10,
        )

    return dcc.Graph(figure=fig)
