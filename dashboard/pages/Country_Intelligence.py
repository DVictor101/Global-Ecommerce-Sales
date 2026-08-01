import streamlit as st
import pandas as pd
import plotly.express as px

#page confiuration
st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Country Analysis")

st.markdown("""
This page analyzes the profitability and sales performance of different countries,
helping identify the strongest markets and opportunities for expansion.
""")

st.markdown("---")

#loading dataset
@st.cache_data
def load_data():
    return pd.read_csv("../data_folder/feature_engineerd_data.csv")

from utils.filters import sidebar_filters

df = load_data()

df = sidebar_filters(df)
##country filter
country = st.selectbox(
    "Select a Country",
    sorted(df["Country"].unique())
)

country_df = df[df["Country"] == country]

#country kpi

total_profit = country_df["Profit"].sum()
average_profit = country_df["Profit"].mean()
transactions = len(country_df)
quantity = country_df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Profit", f"${total_profit:,.2f}")
col2.metric("📦 Quantity Sold", f"{quantity:,}")
col3.metric("🛒 Transactions", f"{transactions:,}")
col4.metric("📈 Average Profit", f"${average_profit:.2f}")

##product by categoy
st.markdown("---")

st.subheader(f"Profit by Category in {country}")

category_profit = (
    country_df
    .groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Profit",
    text_auto=".2s",
    title=f"Category Profit in {country}"
)

st.plotly_chart(fig, use_container_width=True)

#top products
st.markdown("---")

st.subheader(f"Top 10 Products in {country}")

top_products = (
    country_df
    .groupby("Product_Name")["Profit"]
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
    text_auto=".2s"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig, use_container_width=True)

#profit distribution
st.markdown("---")

st.subheader("Profit Distribution")

fig = px.histogram(
    country_df,
    x="Profit",
    nbins=30,
    title="Distribution of Profit"
)

st.plotly_chart(fig, use_container_width=True)

#compare all countries
st.markdown("---")

st.subheader("Country Profit Ranking")

ranking = (
    df
    .groupby("Country")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    ranking,
    x="Country",
    y="Profit",
    color="Profit",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

#country summary table
st.markdown("---")

st.subheader("Country Summary")

summary = (
    df
    .groupby("Country")
    .agg(
        Total_Profit=("Profit", "sum"),
        Average_Profit=("Profit", "mean"),
        Total_Quantity=("Quantity", "sum"),
        Transactions=("Profit", "count")
    )
    .reset_index()
)

st.dataframe(summary, use_container_width=True)

#map showing profitability by country
fig = px.choropleth(
    ranking,
    locations="Country",
    locationmode="country names",
    color="Profit",
    hover_name="Country",
    color_continuous_scale="Viridis",
    title="Global Profit Distribution"
)

st.plotly_chart(fig, use_container_width=True)