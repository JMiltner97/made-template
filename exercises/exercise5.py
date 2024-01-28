import zipfile
import pandas as pd
from urllib.request import urlretrieve
from sqlalchemy import create_engine

data = "https://gtfs.rhoenenergie-bus.de/GTFS.zip"
urlretrieve(data, "GTFS.zip")
with zipfile.ZipFile("GTFS.zip", 'r') as zip:
            zip.extract("stops.txt", '.')
df = pd.read_csv("stops.txt")
df = df.filter(items=['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'zone_id'])
df = df[df['zone_id'] == 2001]
df['valid_coordinates'] = (
    (df['stop_lat'] >= -90) & (df['stop_lat'] <= 90) &
    (df['stop_lon'] >= -180) & (df['stop_lon'] <= 180)
)
df = df[df['valid_coordinates']]
df = df.filter(items=['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'zone_id'])
#print(df)
engine = create_engine("sqlite:///gtfs.sqlite")
df.to_sql(name="stops", con=engine, if_exists="replace", index=False)