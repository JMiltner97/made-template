import pandas as pd
import os
#from pandas import json_normalize
from sqlalchemy import create_engine

#set data target
folder_path = "data"
data_file = "projdata.sqllite"
full_path = os.path.join(folder_path, data_file)

# Declare dataset urls
datasource1 = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46231-0001_00.csv"
datasource2 = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46131-0011_00.xml"
#datasource3 = "https://maps.infoware.de/opendata/roadworks.geojson"

# Create SQLLite DB
engine = create_engine(f"sqlite:///{full_path}")

#read data to df and import
#read in datasource1
try:
    df = pd.read_csv(datasource1, sep=";", encoding='ISO-8859-1')
except UnicodeDecodeError:
    df = pd.read_csv(datasource1, sep=";", encoding='cp1252')
df.to_sql(name="straße", con=engine, if_exists="replace", index=False)

#read in datasource2
df = pd.read_xml(datasource2)
df.to_sql(name="eisenbahn", con=engine, if_exists="replace", index=False)