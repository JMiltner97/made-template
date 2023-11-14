import pandas as pd
from sqlalchemy import create_engine

data = "https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv"
df = pd.read_csv(data, sep=";")
engine = create_engine("sqlite:///airports.sqlite")
df.to_sql(name="airports", con=engine, if_exists="replace", index=False)