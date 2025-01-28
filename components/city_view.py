from dash import Dash, dcc, html, callback, Input, Output, no_update
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import dash_bootstrap_components as dbc

#
# https://cartographyvectors.com/map/1604-new-york-zip-codes
with open("./data/new-york-zip-codes-_1604.geojson") as f:
    zip_geojson = json.load(f)


df = pd.read_csv("./data/NYC_housingOnly_v0.csv")
df["Postal Code"] = df["Postal Code"].astype(str)


def create_choropleth_map(dataframe, color, range_color, labels):
    """
    Creates a choropleth map with customizable range_color and labels.

    Returns:
    - fig: A Plotly choropleth map figure.
    """
    fig = px.choropleth_map(
        data_frame=dataframe,
        color=color,
        range_color=range_color,
        labels=labels,
        geojson=zip_geojson,
        opacity=0.5,
        zoom=10,
        featureidkey="properties.ZCTA5CE10",
        map_style="open-street-map",
        locations="Postal Code",
        center={"lat": 40.7128, "lon": -74.0060},
        height=400,
    )

    # Update layout to match Cyborg theme
    fig.update_layout(
        paper_bgcolor="#060606",  # Primary background color
        plot_bgcolor="#2a2a2a",  # Secondary background color
        font_color="white",  # White font color for contrast
        margin={"r": 10, "t": 25, "l": 10, "b": 10},  # Adjust margins
        coloraxis_colorbar=dict(
            title=dict(
                text=color, font=dict(color="white")  # Colorbar title font color
            ),
            tickcolor="white",  # Colorbar tick color
            tickfont=dict(color="white"),  # Colorbar tick font color
        ),
    )
    return fig


# app = Dash()
city_panel = dbc.Container(
    [
        dcc.Dropdown(
            id="measurments",
            value="ENERGY STAR Score",
            options=[
                "ENERGY STAR Score",
                "Indoor Water Use (All Water Sources) (kgal)",
                "Year Built",
            ],
            style={
                "backgroundColor": "#white",  # Black background
                "color": "#FFFFFF",  # White text
                "border": "1px solid #ffffff",  # Border for consistency with theme
                "border-radius": "4px",  # Rounded corners
                "placeholder": {"color": "#ffffff"},  # White placeholder text
            },
        ),
        dcc.Graph(id="zip-map"),
        html.Div(id="filler"),
    ]
)


@callback(Output("zip-map", "figure"), Input("measurments", "value"))
def make_graph(measurment_chosen):
    df[measurment_chosen] = pd.to_numeric(df[measurment_chosen], errors="coerce")
    df_filtered = df.groupby("Postal Code")[measurment_chosen].mean().reset_index()

    if measurment_chosen == "ENERGY STAR Score":
        fig = create_choropleth_map(
            df_filtered,
            color=measurment_chosen,
            range_color=[35, 75],
            labels={"ENERGY STAR Score": "Energy Score"},
        )
    elif measurment_chosen == "Indoor Water Use (All Water Sources) (kgal)":
        fig = create_choropleth_map(
            df_filtered,
            color=measurment_chosen,
            range_color=[2000, 8000],
            labels={"Indoor Water Use (All Water Sources) (kgal)": "Indoor Water Use"},
        )
    elif measurment_chosen == "Year Built":
        df_filtered["Year Built"] = df_filtered["Year Built"].astype(int)
        fig = create_choropleth_map(
            df_filtered, color=measurment_chosen, range_color=[1925, 1965], labels=None
        )

    return fig


@callback(Output("filler", "children"), Input("zip-map", "clickData"))
def make_graph(clicked_data):
    if clicked_data:
        zipcode = clicked_data["points"][0]["location"]
        df_filtered = df[df["Postal Code"] == zipcode]

        fig = px.scatter_map(
            df_filtered,
            lat="Latitude",
            lon="Longitude",
            hover_name="Year Built",
            zoom=11,
            height=400,
        )
        return dcc.Graph(figure=fig)
    else:
        return no_update


# if __name__ == '__main__':
#     app.run(debug=True)
