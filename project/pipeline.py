import pandas as pd
import geopandas as gpd
from shapely import wkt
import csv


import os

#from pandas import json_normalize
from sqlalchemy import create_engine


csv.field_size_limit(500000)

#set data target

script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
folder_path = os.path.join(parent_dir, "data")
data_file = "projdata.sqlite"
full_path = os.path.join(folder_path, data_file)


# Declare dataset urls
datasource1 = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46231-0001_00.csv"
datasource2 = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46131-0001_00.csv"
datasource3 = "https://maps.infoware.de/opendata/roadworks.geojson"

# Create SQLLite DB
engine = create_engine(f"sqlite:///{full_path}")

#read data to df and import
#read in datasource1
column_names = ['Year',
                'Gewerblicher Verkehr und Werkverkehr insgesamt Beförderte Gütermenge',
                'Gewerblicher Verkehr und Werkverkehr insgesamt Beförderungsleistung',
                'Binnenverkehr Beförderte Gütermenge',
                'Binnenverkehr Beförderungsleistung',
                'Grenzüberschreitender Verkehr Beförderte Gütermenge',
                'Grenzüberschreitender Verkehr Beförderungsleistung',
                'Grenzüberschreitender Versand Beförderte Gütermenge',
                'Grenzüberschreitender Versand Beförderungsleistung',
                'Grenzüberschreitender Empfang Beförderte Gütermenge',
                'Grenzüberschreitender Empfang Beförderungsleistung',
                'Kabotage Beförderte Gütermenge',
                'Kabotage Beförderungsleistung']
try:
    df = pd.read_csv(datasource1, sep=";", encoding='ISO-8859-1', on_bad_lines='skip', engine='python', header=None, names=column_names, skiprows=9,skipfooter=4)
except UnicodeDecodeError:
    df = pd.read_csv(datasource1, sep=";", encoding='cp1252', on_bad_lines='skip', engine='python', header=None, names=column_names, skiprows=9, skipfooter=4)
df.to_sql(name="straße", con=engine, if_exists="replace", index=False)
print(df.tail())

#read in datasource2
column_names = ['Year',
                'Beförderte Güter',
                'Veränderung zum Vorjahr BefGü',
                'Beförderungsleistung',
                'Veränderung zum Vorjahr BefLst']
try:
    df = pd.read_csv(datasource2, sep=";", encoding='ISO-8859-1', on_bad_lines='skip', engine='python', header=None, names=column_names, skiprows=7, skipfooter=3)
except UnicodeDecodeError:
    df = pd.read_csv(datasource2, sep=";", encoding='cp1252', on_bad_lines='skip', engine='python', header=None, names=column_names, skiprows=7, skipfooter=3,)

df.to_sql(name="eisenbahn", con=engine, if_exists="replace", index=False)
print(df.tail())

#read in datasource3
gdf = gpd.read_file(datasource3)
gdf.drop('geometry', axis=1, inplace=True)
gdf.to_sql(name="baustellen", con=engine, if_exists="replace", index=False)