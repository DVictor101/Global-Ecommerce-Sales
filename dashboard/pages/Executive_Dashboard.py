import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_PATH = BASE_DIR / "data_folder" / "Feature_engineered_data.csv"

    df = pd.read_csv(DATA_PATH)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df


df = load_data()


## createing time features
df["Year"] = df["Order_Date"].dt.year

df["Month"] = df["Order_Date"].dt.month_name()

df["Month_Number"] = df["Order_Date"].dt.month

df["Day"] = df["Order_Date"].dt.day

df["Weekday"] = df["Order_Date"].dt.day_name()

#sorting months
month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

df["Month"] = pd.Categorical(
    df["Month"],
    categories=month_order,
    ordered=True
)

#adding year filter
year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["Year"].unique().tolist())
)



st.title("📊 Executive Dashboard")

st.markdown("""
Monitor Global E-Commerce performance through Interactive KPIs and Visualizations""")

## dashboard filters

st.sidebar.header("Dashboard Filters")

country = st.sidebar.selectbox("Country", ["ALL"] + sorted(df["Country"].unique()))
region = st.sidebar.selectbox("Region", ["ALL"] + sorted(df["Region"].unique()))
category = st.sidebar.selectbox("Category", ["ALL"] + sorted(df["Category"].unique()))
sub_category = st.sidebar.selectbox("Sub_Category", ["ALL"] + sorted(df["Sub_Category"].unique()))

#applying filters
filtered_df = df.copy()

if country != "ALL":
    filtered_df = filtered_df[filtered_df["Country"] == country]

if region != "ALL":
    filtered_df = filtered_df[filtered_df["Region"] == region]

if category != "ALL":
    filtered_df = filtered_df[filtered_df["Category"] == category]

if sub_category != "ALL":
    filtered_df = filtered_df[filtered_df["Sub_Category"] == sub_category]

if year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == year
    ]


# quarter filter
quarter = st.sidebar.selectbox(
    "Quarter",
    ["All"] + sorted(df["Quarter"].unique())
)

if quarter != "All":
    filtered_df = filtered_df[
        filtered_df["Quarter"] == quarter
    ]

#season

season = st.sidebar.selectbox(
    "Season",
    ["All"] + sorted(df["Season"].unique())
)

if season != "All":
    filtered_df = filtered_df[
        filtered_df["Season"] == season
    ]

## month

month = st.sidebar.selectbox(
    "Month",
    ["All"] + month_order
)

if month != "All":
    filtered_df = filtered_df[
        filtered_df["Month"] == month
    ]
## KPI Cards

revenue = filtered_df["Revenue"].sum()

profit = filtered_df["Profit"].sum()

orders = len(filtered_df)

countries = filtered_df["Country"].nunique()

profit_margin = (profit / revenue) * 100 if revenue > 0 else 0

average_order = revenue / orders if orders > 0 else 0


#display KPIS

kpi1, kpi2, kpi3 = st.columns(3)

kpi4, kpi5, kpi6 = st.columns(3)

kpi1.metric("Revenue", f"${revenue:,.2f}")
kpi2.metric("Profit", f"${profit:,.2f}")
kpi3.metric("Orders", f"{orders:,}")
kpi4.metric("Countries", f"{countries:,}")
kpi5.metric("Profit Margin", f"{profit_margin:.2f}%")
kpi6.metric("Average Order Value", f"${average_order:,.2f}")

## Revenue trend

st.subheader("Revenue Trend")

monthly_revenue = filtered_df.groupby("Order_Date", as_index=False)["Revenue"].sum()

fig = px.line(monthly_revenue, x="Order_Date", y="Revenue", markers=True)

st.plotly_chart(fig, use_container_width=True)

## profit trend
st.subheader("Profit Trend")

monthly_profit = filtered_df.groupby("Order_Date", as_index=False)["Profit"].sum()

fig = px.line(monthly_profit, x="Order_Date", y="Profit", markers=True)

st.plotly_chart(fig, use_container_width=True)


#Revenue by country

st.subheader("Revenue by Country")

country_rev = filtered_df.groupby("Country", as_index=False)["Revenue"].sum()

fig = px.bar(country_rev, x="Country", y="Revenue", color="Revenue")

st.plotly_chart(fig, use_container_width=True)


## revenue vs profit

st.subheader("Revenue vs Profit")

comparison = filtered_df.groupby("Country", as_index=False)[["Revenue", "Profit"]].sum()

fig = px.scatter(comparison, x="Revenue", y="Profit", size="Revenue", color="Country", hover_name="Country")

st.plotly_chart(fig, use_container_width=True)

monthly = (
    filtered_df
    .groupby(["Year", "Month", "Month_Number"], as_index=False)["Revenue"]
    .sum()
    .sort_values(["Year", "Month_Number"])
)

fig = px.line(
    monthly,
    x="Month",
    y="Revenue",
    color="Year",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)

## profit by country
st.markdown("---")
st.subheader("🌍 Profit by Country")

country_profit = (
    filtered_df
    .groupby("Country", as_index=False)["Profit"]
    .sum()
)

fig = px.choropleth(
    country_profit,
    locations="Country",
    locationmode="country names",
    color="Profit",
    hover_name="Country",
    color_continuous_scale="Viridis",
    title="Global Profit Distribution"
)

st.plotly_chart(fig, use_container_width=True, key="profit_by_country")

##revenue by country
st.markdown("---")
st.subheader("🌍 Profit by Country")

country_profit = (
    filtered_df
    .groupby("Country", as_index=False)["Profit"]
    .sum()
)

fig = px.choropleth(
    country_profit,
    locations="Country",
    locationmode="country names",
    color="Profit",
    hover_name="Country",
    color_continuous_scale="Viridis",
    title="Global Profit Distribution"
)

st.plotly_chart(fig, use_container_width=True, key="revenue_by_country")

#revenue by region
st.subheader("🌎 Revenue by Region")

region_revenue = (
    filtered_df
    .groupby("Region", as_index=False)["Revenue"]
    .sum()
)

fig = px.bar(
    region_revenue,
    x="Region",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    title="Revenue by Region"
)

fig.update_layout(xaxis_title="", yaxis_title="Revenue")

st.plotly_chart(fig, use_container_width=True, key = "revenue_by_region")

#profit by region
st.subheader("💰 Profit by Region")

region_profit = (
    filtered_df
    .groupby("Region", as_index=False)["Profit"]
    .sum()
)

fig = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Profit",
    text_auto=".2s",
    title="Profit by Region"
)

fig.update_layout(xaxis_title="", yaxis_title="Profit")

st.plotly_chart(fig, use_container_width=True, key="profit_by_region")

#top 10 most profitable countries
st.subheader("🏆 Top 10 Most Profitable Countries")

top_countries = (
    filtered_df
    .groupby("Country", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
    .head(10)
)

fig = px.bar(
    top_countries,
    x="Profit",
    y="Country",
    orientation="h",
    color="Profit",
    text_auto=".2s",
    title="Top 10 Countries by Profit"
)

fig.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig, use_container_width=True, key="top_countries")

#bottom 10 least profitable countries
st.subheader("📉 Bottom 10 Least Profitable Countries")

bottom_countries = (
    filtered_df
    .groupby("Country", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit")
    .head(10)
)

fig = px.bar(
    bottom_countries,
    x="Profit",
    y="Country",
    orientation="h",
    color="Profit",
    text_auto=".2s",
    title="Bottom 10 Countries by Profit"
)

fig.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig, use_container_width=True, key="bottom_countries")

  

#profit by category
st.subheader("💵 Profit by Category")

category_profit = (
    filtered_df
    .groupby("Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Profit",
    text_auto=".2s",
    title="Profit by Category"
)

st.plotly_chart(fig, use_container_width=True, key="category_by_profit")

## diisplay top & bottom tables side by side
st.subheader("📋 Country Profit Summary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top 10 Countries")
    st.dataframe(
        top_countries,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.markdown("### 📉 Bottom 10 Countries")
    st.dataframe(
        bottom_countries,
        use_container_width=True,
        hide_index=True
    )

