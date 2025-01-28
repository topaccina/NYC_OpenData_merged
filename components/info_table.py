import dash_ag_grid as dag
import pandas as pd

#
df_info = pd.read_csv(
    "./data/NYC_Community_Boards.csv",
    usecols=[
        "Borough",
        # "Community Board",
        "Neighborhoods",
        # "Latitude",
        # "Longitude",
        "Community Board 1",
        "Postcode",
        # "Location Point",
    ],
)
df_info.rename(columns={"Community Board 1": "Community Board"}, inplace=True)
columnDefs = [{"field": col, "filter": True} for col in df_info.columns]

grid = dag.AgGrid(
    id="getting-started-filter",
    rowData=df_info.to_dict("records"),
    className="ag-theme-alpine-dark",  # Apply dark theme
    style={"height": "400px", "width": "80%"},  # Adjust table size
    columnDefs=columnDefs,
)
