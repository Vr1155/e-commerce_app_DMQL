# app.py
import streamlit as st
import pandas as pd
from utils.db import run_query

st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")
st.title("📊 E-Commerce Analytics Dashboard")

# --- Define organized query sections ---
task5_queries = {
    "Order Status Counts": "order_status_counts.sql",
    "Order Product Details": "order_product_details.sql",
    "High Order Customers": "high_order_customers.sql",
    "Seller Revenue": "seller_revenue.sql",
}

task9_queries = {
    "Customer Geolocation": "customer_geolocation.sql",
    "Seller Count By State": "seller_count_by_state.sql",
    "High Value Payments": "high_value_payments.sql",
    "Top Orders By Freight": "top_orders_by_freight.sql",
}

task8_queries = {
    "Total Orders Per Customer": "total_orders_per_customer.sql",
    "Top 10 Products by Revenue": "top_10_products_by_revenue.sql",
    "Avg Delivery Time per Seller": "avg_delivery_time_per_seller.sql",
    "Recent Orders Last 10 Years": "recent_orders_last_10_years.sql",
    "Review Score 1 Orders": "review_score_1_orders.sql",
}

# --- Sidebar Selection ---
st.sidebar.title("Choose Query Mode")

# --- Switch between Predefined Dashboard and Custom SQL Query
query_mode = st.sidebar.radio(
    "Select Query Mode",
    ("Predefined Dashboard Queries", "Run Your Own SQL Query")
)

if query_mode == "Predefined Dashboard Queries":
    # --- Predefined query selection ---
    st.sidebar.title("Choose a Task and Query")

    task_selected = st.sidebar.radio(
        "Select Task",
        ("Basic SQL Query Exploration (Task 5)", "General Operations and Analysis (Task 9)", "Performance Tuning Queries (Task 8)")
    )

    if task_selected == "Basic SQL Query Exploration (Task 5)":
        selected_query = st.sidebar.selectbox("Select Query", list(task5_queries.keys()))
        query_file = task5_queries[selected_query]

    elif task_selected == "General Operations and Analysis (Task 9)":
        selected_query = st.sidebar.selectbox("Select Query", list(task9_queries.keys()))
        query_file = task9_queries[selected_query]

    else:
        selected_query = st.sidebar.selectbox("Select Query", list(task8_queries.keys()))
        query_file = task8_queries[selected_query]

    # --- Execute and Display Predefined Query ---
    st.subheader(f"🔎 Results: {selected_query}")

    try:
        df = run_query(query_file)
        st.dataframe(df, use_container_width=True)

        # 🔵 Smarter Chart Logic
        if len(df.columns) >= 2:
            if len(df) <= 20000:
                x_col = df.columns[0]
                y_col_candidates = [col for col in df.columns[1:] if pd.api.types.is_numeric_dtype(df[col])]
                if y_col_candidates:
                    y_col = y_col_candidates[0]
                    try:
                        chart_df = df[[x_col, y_col]].dropna()
                        chart_df = chart_df.set_index(x_col)
                        st.bar_chart(chart_df)
                    except Exception as chart_error:
                        st.info("ℹ️ Chart could not be displayed due to plotting issue.")
                else:
                    st.info("ℹ️ No suitable numeric column found for charting.")
            else:
                st.info("ℹ️ Dataset too large (>20000 rows). Chart skipped to avoid crashing.")
        else:
            st.info("ℹ️ Not enough columns to create a chart.")

    except Exception as e:
        st.error(f"❌ Failed to execute query: {e}")

else:
    # --- Divider Line ---
    st.markdown("---")

    # --- User SQL Query Mode ---
    st.header("📝 Run Your Own SQL Query")

    user_query = st.text_area("Enter your SQL query:")

    if st.button("Execute Your Query"):
        if user_query.strip() != "":
            try:
                from utils.db import engine
                with engine.connect() as conn:
                    user_df = pd.read_sql_query(user_query, conn)
                st.success("✅ Query executed successfully!")
                st.dataframe(user_df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Failed to execute your query: {e}")
        else:
            st.warning("⚠️ Please enter a valid SQL query.")
