from sqlalchemy import create_engine
import pandas as pd
import streamlit as st  # 🔵 Import streamlit to use st.secrets

# 🔵 Get DATABASE_URL from Streamlit Secrets
DATABASE_URL = st.secrets["DATABASE_URL"]

# 🔵 Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def load_query(query_filename):
    with open(f"queries/{query_filename}", "r") as file:
        return file.read()

def run_query(query_filename):
    query = load_query(query_filename)
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn)
