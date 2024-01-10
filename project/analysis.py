import os
from sqlalchemy import create_engine, inspect
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm




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
years_df = years_df.rename(columns={'Event_Count': 'Baustellen'})


years_df = years_df.merge(df_eis[['Year', 'Beförderte Güter']], on='Year', how='left')
years_df = years_df.rename(columns={'Beförderte Güter': 'Beförderte Güter Eisenbahn'})
years_df['Beförderte Güter Eisenbahn'] = round(years_df['Beförderte Güter Eisenbahn'] / 1000)

years_df = years_df.merge(df_str[['Year', 'Gewerblicher Verkehr und Werkverkehr insgesamt Beförderte Gütermenge']], on='Year', how='left')
years_df = years_df.rename(columns={'Gewerblicher Verkehr und Werkverkehr insgesamt Beförderte Gütermenge': 'Beförderte Güter Straße'})

years_df.to_sql(name="baustellen_per_year", con=engine, if_exists="replace", index=False)



years_df['Change in Eisenbahn per Event'] = years_df['Beförderte Güter Eisenbahn'].pct_change() / years_df['Baustellen'].pct_change()
years_df['Change in Straße per Event'] = years_df['Beförderte Güter Straße'].pct_change() / years_df['Baustellen'].pct_change()

# Filtering out the first row as percentage change is not defined for the first entry
years_df = years_df.iloc[1:]
years_df = years_df.loc[years_df['Year'] < 2023]

print(years_df.head(20))

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(years_df['Year'], years_df['Beförderte Güter Eisenbahn'], label='Shipment on rails in kTons', marker='o')
plt.plot(years_df['Year'], years_df['Beförderte Güter Straße'], label='Shipment on road in kTons', marker='x')
plt.title('Goods Transported on rail and road in kTons')
plt.xlabel('Year')
plt.ylabel('Weight in kTons')
plt.legend()
plt.grid(True)
plt.show()


#regression analysis on trains 
X = years_df[['Baustellen']]
y = years_df['Beförderte Güter Eisenbahn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")

X = sm.add_constant(X)
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())


#regression analysis on streets 
X = years_df[['Baustellen']]
y = years_df['Beförderte Güter Straße']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")

X = sm.add_constant(X)
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())