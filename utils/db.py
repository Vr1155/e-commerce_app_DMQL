from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'ecommerce_db',
    'user': 'postgres',
    'password': 'postgres'
}

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

def load_query(query_filename):
    query_path = Path("queries") / query_filename
    with open(query_path, "r") as file:
        return file.read()

def run_query(query_filename):
    query = load_query(query_filename)
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn)
