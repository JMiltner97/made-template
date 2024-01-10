import os
from sqlalchemy import create_engine, inspect
import pandas as pd


script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
folder_path = os.path.join(parent_dir, "data")
data_file = "projdata.sqlite"
full_path = os.path.join(folder_path, data_file)

# Create SQLite DB engine
engine = create_engine(f"sqlite:///{full_path}")

table_name_bau = "baustellen"
table_name_eis = "eisenbahn"
table_name_sta = "straße"

query = f"SELECT * FROM {table_name_bau}"
df_bau = pd.read_sql_query(query, engine)
df_bau['startDate'] = pd.to_datetime(df_bau['startDate'])
df_bau['endDate'] = pd.to_datetime(df_bau['endDate'])

query_eis = f"SELECT * FROM {table_name_eis}"
df_eis = pd.read_sql_query(query_eis, engine)

query_str = f"SELECT * FROM {table_name_sta}"
df_str = pd.read_sql_query(query_str, engine)

min_year = df_bau['startDate'].dt.year.min()
max_year = df_bau['endDate'].dt.year.max()
years = range(min_year, max_year)
years_df = pd.DataFrame(years, columns=['Year'])

df_bau['startDate'] = pd.to_datetime(df_bau['startDate'])
df_bau['endDate'] = pd.to_datetime(df_bau['endDate'])

def count_events(year):
    return ((df_bau['startDate'].dt.year <= year) & (df_bau['endDate'].dt.year >= year)).sum()

years_df['Event_Count'] = years_df['Year'].apply(count_events)

years_df = years_df.merge(df_eis[['Year', 'Beförderte Güter']], on='Year', how='left')
years_df = years_df.rename(columns={'Beförderte Güter': 'Beförderte Güter Eisenbahn'})
years_df['Beförderte Güter Eisenbahn'] = round(years_df['Beförderte Güter Eisenbahn'] / 1000)


years_df = years_df.merge(df_str[['Year', 'Gewerblicher Verkehr und Werkverkehr insgesamt Beförderte Gütermenge']], on='Year', how='left')
years_df = years_df.rename(columns={'Gewerblicher Verkehr und Werkverkehr insgesamt Beförderte Gütermenge': 'Beförderte Güter Straße'})

print(years_df.head())

years_df.to_sql(name="baustellen_per_year", con=engine, if_exists="replace", index=False)

