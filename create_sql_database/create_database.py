#Setup
#!pip install pandas sqlalchemy
import sqlite3
import pandas as pd


# Read the CSV file
csv_file = r'C:\Users\mroop\OneDrive\Desktop\Charming Data\NYC_OpenData_merged\data\NYC_housingOnly_Reduced_Agent.csv'

community_board_csv = r'C:\Users\mroop\OneDrive\Desktop\Charming Data\NYC_OpenData_merged\data\NYC_Community_Boards_Agent.csv'

#Convert Dataframe to SQLite Database

from sqlalchemy import create_engine

# Connect to SQLite database (or create it)
engine = create_engine('sqlite:///opendata_sql_database.db', echo=False)
conn = sqlite3.connect('opendata_sql_database.db')
cursor = conn.cursor()

# Convert Housing DataFrame to SQL
# (Optional) If it's a large CSV, try inserting in chunks:
chunksize = 10  # Adjust as needed
for chunk in pd.read_csv(csv_file, chunksize=chunksize, encoding='utf-8'):
    chunk.to_sql('property_energy_data', con=engine, if_exists='append', index=False) #Descriptive name for LLM is needed

# Convert Community Board DataFrame to SQL
# (Optional) If it's a large CSV, try inserting in chunks:
chunksize = 10  # Adjust as needed
for chunk in pd.read_csv(community_board_csv, chunksize=chunksize, encoding='utf-8'):
    chunk.to_sql('community_board_info', con=engine, if_exists='append', index=False)

# Commit and close the connection
conn.commit()
conn.close()


#!pip install -qU langchain langchain-openai langchain-community langchain-experimental pandas
from langchain_community.utilities import SQLDatabase

#Print Database Information
db = SQLDatabase(engine=engine)