import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------
# Page Configuration
# -----------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="centered",
)

st.title("📊 Executive Dashboard")

st.markdown("---")

# -----------------------
# Load Dataset
# -----------------------


@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data_folder" / "feature_engineerd_data.csv"

    # Debugging (remove these after confirming it works)
    st.write("BASE_DIR:", BASE_DIR)
    st.write("DATA_PATH:", DATA_PATH)
    st.write("Exists:", DATA_PATH.exists())

    if not DATA_PATH.exists():
        st.error(f"Dataset not found:\n{DATA_PATH}")
        st.stop()

    return pd.read_csv(DATA_PATH)

df = load_data()


#kipi cards

# -----------------------
# KPI Calculations
# -----------------------

total_profit = df["Profit"].sum()
total_sales = len(df)
average_profit = df["Profit"].mean()
total_countries = df["Country"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Profit", f"${total_profit:,.2f}")

col2.metric("🛒 Total Transactions", f"{total_sales:,}")

col3.metric("📈 Average Profit", f"${average_profit:.2f}")

col4.metric("🌍 Countries", total_countries)

##profit by country

st.markdown("---")

st.subheader("Profit by Country")

country_profit = (
    df.groupby("Country")["Profit"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

fig = px.bar(
    country_profit,
    x="Country",
    y="Profit",
    color="Profit",
    title="Total Profit by Country"
)

st.plotly_chart(fig, use_container_width=True)

##profit by category

st.markdown("---")

st.subheader("Profit by Category")

category_profit = (
    df.groupby("Category")["Profit"]
      .sum()
      .reset_index()
)

fig = px.pie(
    category_profit,
    names="Category",
    values="Profit",
    hole=0.4,
    title="Profit Contribution by Category"
)

st.plotly_chart(fig, use_container_width=True)

##profit by 10 products

st.markdown("---")

st.subheader("Top 10 Most Profitable Products")

top_products = (
    df.groupby("Product_Name")["Profit"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    top_products,
    x="Profit",
    y="Product_Name",
    orientation="h",
    color="Profit",
    title="Top 10 Products by Profit"
)

fig.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig, use_container_width=True)

#monthly profit trend

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

monthly_profit = (
    df.groupby(df["Order_Date"].dt.to_period("M"))["Profit"]
      .sum()
)

monthly_profit.index = monthly_profit.index.astype(str)

fig = px.line(
    monthly_profit,
    title="Monthly Profit Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.write("""
The Executive Dashboard provides a high-level overview of the company's
financial performance. It summarizes key performance indicators (KPIs)
and visualizes profitability across countries, product categories,
and products to support strategic business decisions.
""")