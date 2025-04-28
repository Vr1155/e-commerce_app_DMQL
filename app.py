# new_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import fetch_table
import plotly.graph_objects as go
import requests


st.set_page_config(page_title="E-Commerce Business Intelligence Dashboard", layout="wide")

# --- Sidebar ---
st.sidebar.title("Navigation")
refresh = st.sidebar.button("🔄 Refresh Dashboard")
page = st.sidebar.radio("Go to", ("🏠 Home Dashboard", "📋 Predefined Queries", "📚 Browse Tables", "🛠️ Custom SQL Query"))

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

                    if view_name == "view_avg_delivery_time_per_seller" and 'seller_id' in query_sql.columns and 'avg_delivery_days' in query_sql.columns:
                        top_delays = query_sql.sort_values(by='avg_delivery_days', ascending=False).head(10)
                        fig = px.bar(
                            top_delays,
                            x='seller_id',
                            y='avg_delivery_days',
                            title=f"{query_name}: Top 10 Sellers by Avg Delivery Days",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title="Seller ID",
                            yaxis_title="Avg Delivery Days",
                            margin=dict(l=40, r=40, t=80, b=160)
                        )
                        st.plotly_chart(fig, use_container_width=True)

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

                    elif view_name == "view_order_status_counts" and 'order_status' in query_sql.columns and 'total_orders' in query_sql.columns:
                        fig = px.bar(
                            query_sql.sort_values(by='total_orders', ascending=False),
                            x='order_status',
                            y='total_orders',
                            title=f"{query_name} Overview",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title="Order Status",
                            yaxis_title="Total Orders",
                            margin=dict(l=40, r=40, t=80, b=160)
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif view_name == "view_total_orders_per_customer" and 'customer_id' in query_sql.columns and 'total_orders' in query_sql.columns:
                        st.subheader("📊 Total Orders Per Customer: Summary Statistics")
                        try:
                            stats = fetch_table("view_total_orders_summary").iloc[0]
                            min_val = stats['min_orders']
                            p25_val = stats['p25_orders']
                            median_val = stats['median_orders']
                            p75_val = stats['p75_orders']
                            max_val = stats['max_orders']

                            if min_val == p25_val == median_val == p75_val == max_val:
                                st.metric("Min Orders", f"{min_val:.2f}")
                                st.metric("25th Percentile Orders", f"{p25_val:.2f}")
                                st.metric("Median Orders", f"{median_val:.2f}")
                                st.metric("75th Percentile Orders", f"{p75_val:.2f}")
                                st.metric("Max Orders", f"{max_val:.2f}")
                            else:
                                fig = go.Figure()
                                fig.add_trace(go.Box(
                                    y=[min_val, p25_val, median_val, p75_val, max_val],
                                    boxpoints=False
                                ))
                                fig.update_layout(
                                    title="Total Orders Per Customer: Box Plot Overview",
                                    yaxis_title="Number of Orders",
                                    height=600
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"❌ Failed to plot summary: {e}")

                    elif view_name == "view_top_10_products_by_revenue" and 'product_category_name' in query_sql.columns and 'total_revenue' in query_sql.columns:
                        fig = px.bar(
                            query_sql,
                            x='product_category_name',
                            y='total_revenue',
                            title=f"{query_name}: Revenue by Product Category",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title="Product Category",
                            yaxis_title="Total Revenue",
                            margin=dict(l=40, r=40, t=80, b=160)
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif view_name == "view_recent_orders_last_10_years" and 'order_purchase_timestamp' in query_sql.columns:
                        query_sql['order_purchase_timestamp'] = pd.to_datetime(query_sql['order_purchase_timestamp'])
                        query_sql['order_purchase_month'] = query_sql['order_purchase_timestamp'].dt.to_period('M').dt.to_timestamp()

                        monthly_orders = query_sql.groupby('order_purchase_month').size().reset_index(name='num_orders')

                        fig = px.line(
                            monthly_orders,
                            x='order_purchase_month',
                            y='num_orders',
                            title="Recent Orders Over Last 10 Years (Monthly Trend)",
                            markers=True,
                            height=600
                        )
                        fig.update_layout(
                            xaxis_title="Month",
                            yaxis_title="Number of Orders",
                            margin=dict(l=40, r=40, t=80, b=80)
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif view_name == "view_review_score_1_orders" and 'review_score' in query_sql.columns:
                        review_1_count_row = fetch_table("view_review_score_1_count").iloc[0]
                        total_reviews_row = fetch_table("view_total_reviews").iloc[0]

                        review_1_count = review_1_count_row['review_score_1_count']
                        total_reviews = total_reviews_row['total_reviews']

                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=review_1_count,
                            title={"text": "Review Score 1 Orders vs Total Reviews"},
                            gauge={"axis": {"range": [0, total_reviews]}, "bar": {"color": "red"}},
                            number={"suffix": f" / {total_reviews}"}
                        ))
                        st.plotly_chart(fig, use_container_width=True)

                    elif view_name == "view_customer_geolocation" and 'customer_latitude' in query_sql.columns and 'customer_longitude' in query_sql.columns:
                        fig = px.scatter_mapbox(
                            query_sql,
                            lat="customer_latitude",
                            lon="customer_longitude",
                            zoom=3,
                            center={"lat": -14.2350, "lon": -51.9253},
                            height=700,
                            mapbox_style="carto-positron",
                            title="Customer Geolocation Map Overview"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif view_name == "view_seller_count_by_state" and 'seller_zip_code_prefix' in query_sql.columns and 'seller_count' in query_sql.columns:
                        seller_geo = fetch_table("view_seller_geolocation")
                        merged = pd.merge(query_sql, seller_geo, on="seller_zip_code_prefix", how="left")

                        fig = px.scatter_mapbox(
                            merged,
                            lat="seller_latitude",
                            lon="seller_longitude",
                            size="seller_count",
                            color="seller_count",
                            size_max=30,
                            color_continuous_scale="Viridis",
                            zoom=3,
                            center={"lat": -14.2350, "lon": -51.9253},
                            height=700,
                            mapbox_style="carto-positron",
                            title="Seller Count Distribution by Location"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif view_name == "view_high_value_payments" and 'payment_value' in query_sql.columns:
                        top_payments = query_sql.sort_values(by='payment_value', ascending=False).head(10)

                        fig = px.bar(
                            top_payments,
                            x='order_id',
                            y='payment_value',
                            title="Top 10 High Value Payments",
                            height=600
                        )
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title="Order ID",
                            yaxis_title="Payment Value",
                            yaxis_tickprefix="$",
                            yaxis_tickformat=",",
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
    st.header("🏠 E-Commerce Business Intelligence Dashboard")
    with st.spinner("Loading Dashboard Insights..."):
        # Load data
        sellers = get_cached_table("sellers")
        orders = get_cached_table("orders")
        order_items = get_cached_table("order_items")
        payments = get_cached_table("order_payments")
        reviews = get_cached_table("order_reviews")
        products = get_cached_table("products")

        # --- Updated KPI Cards ---
        st.subheader("📋 Key Metrics")
        kpi_data = get_cached_table("view_dashboard_kpis").iloc[0]

        k1, k2, k3 = st.columns(3)
        k1.metric("Total Customers", f"{int(kpi_data['total_customers']):,}")
        k2.metric("Total Orders", f"{int(kpi_data['total_orders']):,}")
        k3.metric("Average Payment", f"${kpi_data['avg_payment']:.2f}")

        k4, k5, k6 = st.columns(3)
        k4.metric("Average Review Score", f"{kpi_data['avg_review_score']:.2f} ⭐")
        k5.metric("Total Revenue", f"${kpi_data['total_revenue']:,.2f}")
        k6.metric("Total Freight Value", f"${kpi_data['total_freight']:,.2f}")

        k7, k8, k9 = st.columns(3)
        k7.metric("5-Star Reviews", f"{int(kpi_data['five_star_reviews']):,}")
        k8.metric("Total Sellers", f"{int(kpi_data['total_sellers']):,}")
        k9.metric("Total Products", f"{int(kpi_data['total_products']):,}")


        st.subheader("🗺️ Locations by Seller Count")
        if 'seller_zip_code_prefix' in sellers.columns:
            seller_state = sellers.dropna(subset=['seller_zip_code_prefix'])
            seller_state['seller_zip_code_prefix'] = seller_state['seller_zip_code_prefix'].astype(str)
            seller_state = seller_state.groupby('seller_zip_code_prefix').size().reset_index(name='seller_count')

            seller_geo = get_cached_table("view_seller_geolocation")
            merged = pd.merge(seller_state, seller_geo, on="seller_zip_code_prefix", how="left")

            fig = px.scatter_mapbox(
                merged,
                lat="seller_latitude",
                lon="seller_longitude",
                size="seller_count",
                color="seller_count",
                size_max=30,
                color_continuous_scale="Viridis",
                zoom=3,
                center={"lat": -14.2350, "lon": -51.9253},
                height=700,
                mapbox_style="carto-positron",
                title="Seller Count Distribution by Location"
            )
            st.plotly_chart(fig, use_container_width=True)


        st.subheader("💳 Payment vs Freight")
        if 'price' in order_items.columns and 'freight_value' in order_items.columns:
            fig2 = px.scatter(
                order_items,
                x='price',
                y='freight_value',
                title="Price vs Freight Value (All Data)",
                height=600
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🚚 Average Freight Value by Seller Zip Code")

        merged_seller_freight = pd.merge(order_items, sellers, on='seller_id')
        merged_seller_freight = merged_seller_freight.dropna(subset=['seller_zip_code_prefix'])
        merged_seller_freight['seller_zip_code_prefix'] = merged_seller_freight['seller_zip_code_prefix'].astype(str)
        avg_freight_by_zip = merged_seller_freight.groupby('seller_zip_code_prefix')['freight_value'].mean().reset_index()

        # Merge with geolocation
        seller_geo = get_cached_table("view_seller_geolocation")
        merged = pd.merge(avg_freight_by_zip, seller_geo, on="seller_zip_code_prefix", how="left")

        fig = px.scatter_mapbox(
            merged,
            lat="seller_latitude",
            lon="seller_longitude",
            size="freight_value",
            color="freight_value",
            size_max=30,
            color_continuous_scale="Plasma",
            zoom=3,
            center={"lat": -14.2350, "lon": -51.9253},
            height=700,
            mapbox_style="carto-positron",
            title="Average Freight Value by Seller Zip Code (Map Visualization)"
        )
        st.plotly_chart(fig, use_container_width=True)


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
elif page == "🛠️ Custom SQL Query":
    st.header("🛠️ Custom SQL Query Executor")

    custom_query = st.text_area("Write your SQL query here:", height=150)

    if st.button("Run Query"):
        try:
            query_to_execute = custom_query.strip().rstrip(';')  # ✅ Fix semicolon problem

            url = f"{st.secrets['SUPABASE_URL']}/rest/v1/rpc/run_custom_query"
            headers = {
                "apikey": st.secrets["SUPABASE_API_KEY"],
                "Authorization": f"Bearer {st.secrets['SUPABASE_API_KEY']}",
                "Content-Type": "application/json"
            }
            payload = {"query_text": query_to_execute}

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and 'message' in data[0]:
                    st.success(data[0]['message'])
                elif data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("⚠️ Query executed but returned no results.")
            else:
                st.error(f"❌ Query failed: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"❌ Error executing query: {e}")

else:
    try:
        with st.spinner("Opening Browse Tables View..."):
            browse_tables()
    except Exception as e:
        st.error(f"❌ Failed to load Browse Tables view: {e}")
