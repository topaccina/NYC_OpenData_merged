import dash_ag_grid as dag
import pandas as pd

#
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

columnDefs = [{"field": col, "filter": True} for col in df_info.columns]

grid = dag.AgGrid(
    id="getting-started-filter",
    rowData=df_info.to_dict("records"),
    columnDefs=columnDefs,
)
