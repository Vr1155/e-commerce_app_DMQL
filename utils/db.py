# utils/db.py

import requests
import streamlit as st
import pandas as pd

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]

def fetch_table(table_name, select_columns="*", filters=None):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"  # 🚨 NO SCHEMA prefix here
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "select": select_columns
    }
    if filters:
        params.update(filters)

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        st.error(f"Failed to fetch {table_name}: {response.status_code} - {response.text}")
        return pd.DataFrame()
