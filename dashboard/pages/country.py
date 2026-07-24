import streamlit as st
import pandas as pd
import plotly.express as px

#load data

@st.cache_data
def load_data():
    df = pd.read_csv("../data_folder/Feature_engineered_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

#title
st.title("🌍 Country Intelligence")

st.markdown("""
Identify the most profitable countries for business expansion
using sales, profit and customer metrics.
""")

#sidebar
country = st.sidebar.selectbox(
    "Country",
    sorted(df["Country"].unique())
)

#filter
country_df = df[
    df["Country"] == country
]

#country kapi
#revenue

revenue = country_df["Revenue"].sum()

#profit
profit = country_df["Profit"].sum()

#orders
orders = len(country_df)

#customers
customers = country_df["Customer_ID"].nunique()

#average order
average_order = revenue/orders

#profit margin
profit_margin = profit/revenue*100

#displaying our data
k1,k2,k3 = st.columns(3)

k4,k5,k6 = st.columns(3)

k1.metric("Revenue",f"${revenue:,.0f}")

k2.metric("Profit",f"${profit:,.0f}")

k3.metric("Orders",orders)

k4.metric("Customers",customers)

k5.metric("Average Order",f"${average_order:,.2f}")

k6.metric("Profit Margin",f"{profit_margin:.2f}%")

#monthly revenue trend
monthly = (
    country_df
    .groupby("Order_Date",as_index=False)["Revenue"]
    .sum()
)

fig = px.line(
    monthly,
    x="Order_Date",
    y="Revenue",
    markers=True
)

st.plotly_chart(fig,use_container_width=True)

#monthly profit trend
monthly = (
    country_df
    .groupby("Order_Date",as_index=False)["Profit"]
    .sum()
)

fig = px.line(
    monthly,
    x="Order_Date",
    y="Profit",
    markers=True
)

st.plotly_chart(fig,use_container_width=True)

#category perfoemance
category = (
    country_df
    .groupby("Category",as_index=False)
    .agg({
        "Revenue":"sum",
        "Profit":"sum"
    })
)

#revenue
fig = px.bar(
    category,
    x="Category",
    y="Revenue",
    color="Revenue"
)

st.plotly_chart(fig,use_container_width=True)
#profit
fig = px.bar(
    category,
    x="Category",
    y="Profit",
    color="Profit"
)

st.plotly_chart(fig,use_container_width=True)

##top products

products = (
    country_df
    .groupby("Product_Name",as_index=False)
    .agg({
        "Revenue":"sum",
        "Profit":"sum"
    })
    .sort_values(
        "Profit",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    products,
    x="Profit",
    y="Product_Name",
    orientation="h",
    color="Profit"
)

st.plotly_chart(fig,use_container_width=True)

#customer segment

segment = (
    country_df
    .groupby("Customer_Segment",as_index=False)
    .agg({
        "Revenue":"sum",
        "Profit":"sum"
    })
)

fig = px.pie(
    segment,
    names="Customer_Segment",
    values="Profit"
)

st.plotly_chart(fig,use_container_width=True)

#payment menthod
payment = (
    country_df
    .groupby("Payment_Method",as_index=False)
    .agg({
        "Profit":"sum"
    })
)
fig = px.bar(
    payment,
    x="Payment_Method",
    y="Profit",
    color="Profit"
)

st.plotly_chart(fig,use_container_width=True)


#shipping method
shipping = (
    country_df
    .groupby("Shipping_Method",as_index=False)
    .agg({
        "Profit":"sum"
    })
)
fig = px.bar(
    shipping,
    x="Shipping_Method",
    y="Profit",
    color="Profit"
)

st.plotly_chart(fig,use_container_width=True)

# AI BUSINES RECOMMENDATION
top_category = (
    category
    .sort_values("Profit",ascending=False)
    .iloc[0]
)

top_product = (
    products
    .iloc[0]
)

top_segment = (
    segment
    .sort_values("Profit",ascending=False)
    .iloc[0]
)

#DISPLAY
st.success(f"""
## Business Recommendation

📍 Country: **{country}**

✅ Total Profit: **${profit:,.0f}**

✅ Profit Margin: **{profit_margin:.2f}%**

📦 Best Category:
**{top_category['Category']}**

🛍 Best Product:
**{top_product['Product_Name']}**

👥 Most Profitable Customer Segment:
**{top_segment['Customer_Segment']}**

### Recommendation

This market demonstrates strong profitability and customer demand.
Investment should prioritize the **{top_category['Category']}** category while focusing marketing efforts on the **{top_segment['Customer_Segment']}** customer segment.
""")