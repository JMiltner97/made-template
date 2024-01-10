import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

# Init
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
folder_path = os.path.join(parent_dir, "data")
data_file = "projdata.sqlite"
full_path = os.path.join(folder_path, data_file)

# Create SQLite DB engine
engine = create_engine(f"sqlite:///{full_path}")

# Table names to check
table_names = ["straße", "eisenbahn", "baustellen"]

# Create an Inspector object
inspector = inspect(engine)

# Check each table
for table_name in table_names:
    try:
        # Query the database to check if the table exists
        exists = inspector.has_table(table_name)  # Pass only the table name
        print(f"Table '{table_name}': {'Exists' if exists else 'Does Not Exist'}")
    except SQLAlchemyError as e:
        print(f"Error checking table {table_name}: {e}")
