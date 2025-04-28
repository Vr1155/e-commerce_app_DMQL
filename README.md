# 🛍️ E-Commerce Dashboard - Streamlit App

Welcome to the E-Commerce Analytics Dashboard! 📊🚀  
This project analyzes and visualizes an E-Commerce dataset using **Streamlit**, **Supabase**, **Plotly**, and **Pandas**.

You can explore customer behavior, seller activity, payments, reviews, and logistics trends through dynamic charts and maps!

---

## 🚀 Live App

👉 [Launch Dashboard Here]([https://your-streamlit-cloud-app-link](https://e-commerce-app-dmql.streamlit.app/))

---

## 📊 Features

- 📋 **Home Dashboard** with 9 Key Business KPIs
- 🗺️ **Customer and Seller Geolocation Maps** (with dynamic dot sizes)
- 📦 **Freight and Payment Analysis**
- 📈 **Monthly Order Trends Over 10 Years**
- 🎯 **Top 10 High Value Payments Visualization**
- 🌟 **Review Score 1 Analysis with Gauge Chart**
- 📚 **Interactive Table Browser for Orders, Products, Payments, Reviews**
- ⚡ **Supabase integration** for real-time backend queries
- 🔥 Highly responsive and beautiful layout!

---

## 🛠️ Tech Stack

| Technology | Purpose |
|:-----------|:--------|
| Streamlit | Frontend Web Application |
| Supabase | Backend Database (Postgres) |
| Plotly | Advanced Interactive Charts |
| Pandas | Data manipulation and summarization |
| Requests | API calls to Supabase RESTful endpoints |

---

## 📂 Project Structure

```
/your-repo-name
 ├── app.py  # Main Streamlit app
 ├── requirements.txt  # List of Python packages
 ├── /utils
 │     └── db.py  # Database utility to fetch tables
 ├── .streamlit/
 │     └── secrets.toml  # (Not pushed to GitHub, used for Supabase credentials)
```

---

## 🔑 Secrets Setup

For local development, create a `.streamlit/secrets.toml` file:

```toml
[general]
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_API_KEY = "your-supabase-service-role-key"
```

In Streamlit Cloud, paste these secrets manually in **Settings > Secrets**.

---

## 📈 Example KPIs

| Metric | Sample Value |
|:-------|:-------------|
| Total Customers | 99,235 |
| Total Orders | 123,456 |
| Average Payment | $156.47 |
| Average Review Score | 4.45 ⭐ |
| Total Revenue | $4,502,000.00 |
| Total Freight Value | $238,000.00 |

---

## 📜 Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. Install the required libraries:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
streamlit run app.py
```

4. For deployment, connect your GitHub repo to [Streamlit Cloud](https://streamlit.io/cloud).

---
## 💬 Acknowledgements

- Thanks to [Streamlit](https://streamlit.io) for making rapid app development simple!
- Thanks to [Supabase](https://supabase.io) for the amazing Postgres-as-a-service platform!

---

## ⭐ How to Contribute

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

# 📢 Star this repository 🌟 if you like the project!

---
