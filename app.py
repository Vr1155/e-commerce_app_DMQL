# --- Sidebar Selection ---
st.sidebar.title("Choose Query Mode")

# --- Switch between Predefined and Custom Query
query_mode = st.sidebar.radio(
    "Select Query Mode",
    ("Predefined Dashboard Queries", "Run Your Own SQL Query")
)

if query_mode == "Predefined Dashboard Queries":
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

    # --- Extra Section: Run Your Own SQL Query ---
    st.header("📝 Run Your Own SQL Query")

    # Text area for user to input query
    user_query = st.text_area("Enter your SQL query:")

    # Button to run the query
    if st.button("Execute Your Query"):
        if user_query.strip() != "":
            try:
                from utils.db import engine  # using the same engine from db.py
                with engine.connect() as conn:
                    user_df = pd.read_sql_query(user_query, conn)
                st.success("✅ Query executed successfully!")
                st.dataframe(user_df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Failed to execute your query: {e}")
        else:
            st.warning("⚠️ Please enter a valid SQL query.")
