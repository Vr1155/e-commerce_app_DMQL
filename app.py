# new_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import fetch_table

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("🏠 Home Dashboard", "📋 Predefined Queries", "📚 Browse Tables"))

# --- Helper Functions ---
def show_kpis():
    st.header("📊 Key Performance Indicators")
    try:
        with st.spinner("Loading KPIs..."):
            customers_df = fetch_table("customers")
            orders_df = fetch_table("orders")
            payments_df = fetch_table("order_payments")
            reviews_df = fetch_table("order_reviews")

            total_customers = len(customers_df)
            total_orders = len(orders_df)
            avg_payment = payments_df['payment_value'].mean()
            avg_review = reviews_df['review_score'].mean()

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric(label="Total Customers", value=f"{total_customers}")
            kpi2.metric(label="Total Orders", value=f"{total_orders}")
            if avg_payment > 100:
                delta_color = "normal"
            elif avg_payment < 50:
                delta_color = "inverse"
            else:
                delta_color = "off"
            kpi3.metric(label="Average Payment", value=f"${avg_payment:.2f}", delta_color=delta_color)
            kpi4.metric(label="Average Review Score", value=f"{avg_review:.2f} ⭐")

            st.toast("✅ KPIs loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load KPIs: {e}")

def show_home_charts():
    st.header("📈 Business Insights")

    try:
        with st.spinner("Loading Seller State Chart..."):
            sellers_df = fetch_table("sellers")
            if 'seller_zip_code_prefix' in sellers_df.columns:
                seller_state = sellers_df.groupby('seller_zip_code_prefix').size().reset_index(name='seller_count')
                fig = px.bar(seller_state, x='seller_zip_code_prefix', y='seller_count', title='Top States by Seller Count')
                st.plotly_chart(fig, use_container_width=True)
            st.toast("✅ Seller State Chart loaded.")
    except Exception as e:
        st.warning(f"⚠️ Could not load Seller State Chart: {e}")

    try:
        with st.spinner("Loading Payment Type Distribution..."):
            payments_df = fetch_table("order_payments")
            if 'payment_type' in payments_df.columns:
                payment_type = payments_df['payment_type'].value_counts().reset_index()
                payment_type.columns = ['payment_type', 'count']
                fig2 = px.pie(payment_type, names='payment_type', values='count', title='Payment Type Distribution')
                st.plotly_chart(fig2, use_container_width=True)
            st.toast("✅ Payment Type Chart loaded.")
    except Exception as e:
        st.warning(f"⚠️ Could not load Payment Type Chart: {e}")

def run_predefined_queries():
    st.header("📋 Predefined Analytical Queries")

    task = st.selectbox("Select Task", ["Task 5: Basic Exploration", "Task 8: Performance Tuning", "Task 9: CRUD Validation"])

    if task == "Task 5: Basic Exploration":
        table = st.selectbox("Select Table", ["orders", "order_items", "products"])
    elif task == "Task 8: Performance Tuning":
        table = st.selectbox("Select Table", ["order_items", "orders", "order_reviews"])
    else:
        table = st.selectbox("Select Table", ["customers", "sellers", "order_payments"])

    try:
        with st.spinner("Fetching data..."):
            df = fetch_table(table)
            if df.empty:
                st.warning("⚠️ No data found!")
            else:
                st.dataframe(df, use_container_width=True)
                st.toast("✅ Data loaded successfully!")

                rows_per_page = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
                for i in range(0, len(df), rows_per_page):
                    st.dataframe(df.iloc[i:i+rows_per_page])

                if df.shape[1] >= 2 and df.shape[0] <= 20000:
                    x = st.selectbox("Select X-axis", df.columns)
                    y = st.selectbox("Select Y-axis", df.columns)
                    fig = px.bar(df, x=x, y=y, title=f"{table} Overview")
                    st.plotly_chart(fig, use_container_width=True)

                st.download_button("Download Results", data=df.to_csv(index=False), file_name=f"{table}_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Failed to load table: {e}")

def browse_tables():
    st.header("📚 Browse Tables")
    st.warning("⚠️ In API mode, custom SQL is not supported. You can browse tables instead.")

    try:
        table = st.selectbox("Select Table to View", ["customers", "orders", "order_items", "products", "order_reviews", "order_payments", "sellers", "geolocation"])
        with st.spinner("Fetching table data..."):
            df = fetch_table(table)
            if df.empty:
                st.warning("⚠️ No data found!")
            else:
                st.dataframe(df, use_container_width=True)
                st.download_button("Download Table", data=df.to_csv(index=False), file_name=f"{table}_full.csv", mime="text/csv")
                st.toast("✅ Table loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load table: {e}")

# --- Main Page Switch ---
if page == "🏠 Home Dashboard":
    try:
        with st.spinner("Loading Home Dashboard..."):
            show_kpis()
            show_home_charts()
        st.success("✅ Home Dashboard loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load Home Dashboard: {e}")

elif page == "📋 Predefined Queries":
    try:
        with st.spinner("Loading Predefined Queries..."):
            run_predefined_queries()
        st.success("✅ Predefined Queries loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load Predefined Queries: {e}")

else:
    try:
        with st.spinner("Opening Browse Tables View..."):
            browse_tables()
    except Exception as e:
        st.error(f"❌ Failed to load Browse Tables view: {e}")
