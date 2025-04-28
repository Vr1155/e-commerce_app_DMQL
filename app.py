# new_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import fetch_table

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# --- Sidebar ---
st.sidebar.title("Navigation")
refresh = st.sidebar.button("🔄 Refresh Dashboard")
page = st.sidebar.radio("Go to", ("🏠 Home Dashboard", "📋 Predefined Queries", "📚 Browse Tables"))

# --- Helper Functions ---
@st.cache_data(ttl=60)
def get_cached_table(table_name):
    return fetch_table(table_name)

def load_sql_query(filename):
    with open(f"queries/{filename}", "r") as f:
        return f.read()


def show_kpis():
    st.header("📊 Key Performance Indicators")
    try:
        with st.spinner("Loading KPIs..."):
            customers_df = get_cached_table("customers")
            orders_df = get_cached_table("orders")
            payments_df = get_cached_table("order_payments")
            reviews_df = get_cached_table("order_reviews")

            total_customers = len(customers_df)
            total_orders = len(orders_df)
            avg_payment = payments_df['payment_value'].mean()
            avg_review = reviews_df['review_score'].mean()

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric(label="Total Customers", value=f"{total_customers}")
            kpi2.metric(label="Total Orders", value=f"{total_orders}")
            delta_color = "normal" if avg_payment > 100 else ("inverse" if avg_payment < 50 else "off")
            kpi3.metric(label="Average Payment", value=f"${avg_payment:.2f}", delta_color=delta_color)
            kpi4.metric(label="Average Review Score", value=f"{avg_review:.2f} ⭐")

            # Sparkline Chart for Orders
            st.subheader("📈 Orders Over Time")
            if "order_purchase_timestamp" in orders_df.columns:
                orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
                trend = orders_df.set_index('order_purchase_timestamp').resample('M').size()
                fig = px.line(x=trend.index, y=trend.values, labels={'x':'Date', 'y':'Orders'}, title="Monthly Orders Trend")
                st.plotly_chart(fig, use_container_width=True)

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

    task5_queries = {
        "Order Status Counts": "view_order_status_counts",
        "Order Product Details": "view_order_product_details",
        "High Order Customers": "view_high_order_customers",
        "Seller Revenue": "view_seller_revenue",
    }

    task8_queries = {
        "Total Orders Per Customer": "view_total_orders_per_customer",
        "Top 10 Products by Revenue": "view_top_10_products_by_revenue",
        "Avg Delivery Time per Seller": "view_avg_delivery_time_per_seller",
        "Recent Orders Last 10 Years": "view_recent_orders_last_10_years",
        "Review Score 1 Orders": "view_review_score_1_orders",
    }

    task9_queries = {
        "Customer Geolocation": "view_customer_geolocation",
        "Seller Count By State": "view_seller_count_by_state",
        "High Value Payments": "view_high_value_payments",
        "Top Orders By Freight": "view_top_orders_by_freight",
    }

    task_option = st.selectbox("Select Task", ["Task 5: Basic Exploration", "Task 8: Performance Tuning", "Task 9: CRUD Validation"])

    queries = {}
    if task_option == "Task 5: Basic Exploration":
        queries = task5_queries
    elif task_option == "Task 8: Performance Tuning":
        queries = task8_queries
    elif task_option == "Task 9: CRUD Validation":
        queries = task9_queries

    query_name = st.selectbox("Select Query", list(queries.keys()))

    try:
        with st.spinner("Running query..."):
            view_name = queries[query_name]

            if view_name == "view_high_order_customers":
                location_data = fetch_table("view_high_order_customers")

                if location_data.empty:
                    st.warning("⚠️ No customers found with more than 1 order!")
                else:
                    fig = px.scatter_mapbox(
                        location_data,
                        lat='geolocation_lat',
                        lon='geolocation_lng',
                        size='total_orders',
                        color='total_orders',
                        color_continuous_scale='Blues',
                        size_max=20,
                        zoom=3,
                        height=800,
                        center={"lat": -14.2350, "lon": -51.9253},
                        mapbox_style="carto-positron",
                        title="High Order Customers Distribution in Brazil"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.toast("✅ Heatmap generated successfully!")
            else:
                query_sql = fetch_table(view_name)

                if query_sql.empty:
                    st.warning("⚠️ No data returned from query!")
                else:
                    st.dataframe(query_sql, use_container_width=True)
                    st.toast("✅ Query executed successfully!")

                    if view_name == "view_order_product_details" and 'product_category_name' in query_sql.columns and 'price' in query_sql.columns:
                        fig = px.bar(
                            query_sql,
                            x='product_category_name',
                            y='price',
                            title=f"{query_name}: Price by Product Category",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title="Product Category",
                            yaxis_title="Price",
                            margin=dict(l=40, r=40, t=80, b=160)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    elif view_name == "view_seller_revenue" and 'seller_id' in query_sql.columns and 'total_revenue' in query_sql.columns:
                        top_sellers = query_sql.sort_values(by='total_revenue', ascending=False).head(20)
                        fig = px.bar(
                            top_sellers,
                            x='seller_id',
                            y='total_revenue',
                            title=f"{query_name}: Top 20 Sellers by Revenue",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title="Seller ID",
                            yaxis_title="Total Revenue",
                            margin=dict(l=40, r=40, t=80, b=160)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = px.bar(
                            query_sql.sort_values(by=query_sql.columns[1], ascending=False),
                            x=query_sql.columns[0],
                            y=query_sql.columns[1],
                            title=f"{query_name} Overview",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title=query_sql.columns[0],
                            yaxis_title=query_sql.columns[1],
                            margin=dict(l=40, r=40, t=80, b=160)
                        )
                        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Failed to execute query: {e}")

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
                search = st.text_input("🔍 Search Table")
                if search:
                    df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

                st.dataframe(df, use_container_width=True)
                st.download_button("Download Table", data=df.to_csv(index=False), file_name=f"{table}_full.csv", mime="text/csv")
                st.toast("✅ Table loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load table: {e}")

# --- Main Page Switch ---
if refresh:
    st.cache_data.clear()
    st.rerun()

# --- Home Dashboard ---
if page == "🏠 Home Dashboard":
    st.header("🏠 Home Dashboard")
    with st.spinner("Loading Dashboard Insights..."):
        # Load data
        sellers = get_cached_table("sellers")
        orders = get_cached_table("orders")
        order_items = get_cached_table("order_items")
        payments = get_cached_table("order_payments")
        reviews = get_cached_table("order_reviews")
        products = get_cached_table("products")

        # KPI Cards
        st.subheader("📋 Key Metrics")
        kpi1, kpi2, kpi3 = st.columns(3)
        total_revenue = order_items['price'].sum()
        total_freight = order_items['freight_value'].sum()
        total_reviews = len(reviews)
        kpi1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
        kpi2.metric(label="Total Freight Value", value=f"${total_freight:,.2f}")
        kpi3.metric(label="Total Reviews", value=f"{total_reviews}")

        st.subheader("🗺️ States by Seller Count")
        if 'seller_zip_code_prefix' in sellers.columns:
            seller_state = sellers.dropna(subset=['seller_zip_code_prefix'])
            seller_state['seller_zip_code_prefix'] = seller_state['seller_zip_code_prefix'].astype(str)
            seller_state = seller_state.groupby('seller_zip_code_prefix').size().reset_index(name='seller_count')
            seller_state = seller_state.sort_values('seller_count', ascending=False)
            fig1 = px.bar(seller_state, x='seller_zip_code_prefix', y='seller_count', title='Seller Count by Zip Code', height=500)
            st.plotly_chart(fig1, use_container_width=True)


        # Payment Value vs Freight Value (Filtered)
        st.subheader("💵 Payment vs Freight")
        merged = pd.merge(order_items, payments, on='order_id')
        filtered = merged[(merged['price'] > 0) & (merged['freight_value'] > 0)]
        if len(filtered) > 1000:
            filtered = filtered.sample(n=1000, random_state=42)
        fig2 = px.scatter(filtered, x='price', y='freight_value', title='Price vs Freight Value (Sampled)', height=500)
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🚚 Average Freight Value by Seller Zip Code")
        merged_seller_freight = pd.merge(order_items, sellers, on='seller_id')
        merged_seller_freight = merged_seller_freight.dropna(subset=['seller_zip_code_prefix'])
        merged_seller_freight['seller_zip_code_prefix'] = merged_seller_freight['seller_zip_code_prefix'].astype(str)
        avg_freight_by_zip = merged_seller_freight.groupby('seller_zip_code_prefix')['freight_value'].mean().reset_index()
        avg_freight_by_zip = avg_freight_by_zip.sort_values('freight_value', ascending=False).head(10)
        fig_new = px.bar(avg_freight_by_zip, x='seller_zip_code_prefix', y='freight_value', title='Top 10 Seller Zip Codes by Avg Freight Value')
        st.plotly_chart(fig_new, use_container_width=True)


        # Average Review Score by Payment Type
        st.subheader("⭐ Average Review Score by Payment Type")
        if 'payment_type' in payments.columns:
            payment_reviews = pd.merge(payments, reviews, on='order_id')
            avg_review_payment = payment_reviews.groupby('payment_type')['review_score'].mean().reset_index()
            fig3 = px.bar(avg_review_payment, x='payment_type', y='review_score', title='Average Review Score by Payment Type')
            st.plotly_chart(fig3, use_container_width=True)

        # Monthly Order Volume Growth
        st.subheader("📅 Monthly Order Volume Growth")
        if 'order_purchase_timestamp' in orders.columns:
            orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
            monthly_orders = orders.set_index('order_purchase_timestamp').resample('M').size().reset_index(name='order_count')
            fig4 = px.line(monthly_orders, x='order_purchase_timestamp', y='order_count', title='Monthly Orders Trend')
            st.plotly_chart(fig4, use_container_width=True)

        # Review Score Distribution
        st.subheader("📊 Review Score Distribution")
        review_dist = reviews['review_score'].value_counts().reset_index()
        review_dist.columns = ['review_score', 'count']
        fig5 = px.pie(review_dist, names='review_score', values='count', title='Review Score Distribution')
        st.plotly_chart(fig5, use_container_width=True)

        # Top 5 Product Categories by Revenue
        st.subheader("🛍️ Top 5 Product Categories by Revenue")
        if 'product_category_name' in products.columns:
            merged_prod = pd.merge(order_items, products, on='product_id')
            top_categories = merged_prod.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(5).reset_index()
            fig6 = px.bar(top_categories, x='product_category_name', y='price', title='Top 5 Product Categories by Revenue')
            st.plotly_chart(fig6, use_container_width=True)

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
