import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("../data_folder/Feature_engineered_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()
filtered_df = df.copy()

#customer dashboard title
st.title("👥 Customer Intelligence")

st.markdown("""
Understand customer behaviour, purchasing patterns,
and profitability across customer groups.
""")

#sidebar filers
country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(filtered_df["Country"].unique())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(filtered_df["Region"].unique())
)

##custimer kpis
customers = filtered_df["Customer_ID"].nunique()


#average revenue per customer
avg_customer_revenue = (
     filtered_df["Revenue"].sum() /
    customers
)

# average profit per customer
avg_customer_profit = (
    filtered_df["Profit"].sum() /
    customers
)

#average orders per customer

orders_per_customer = (
    len(filtered_df) /
    customers
)

## displaying the information

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Customers",
    f"{customers:,}"
)

k2.metric(
    "Revenue / Customer",
    f"${avg_customer_revenue:,.2f}"
)

k3.metric(
    "Profit / Customer",
    f"${avg_customer_profit:,.2f}"
)

k4.metric(
    "Orders / Customer",
    f"{orders_per_customer:.2f}"
)


#customer segment analysis
segment = (
    filtered_df
    .groupby("Customer_Segment", as_index=False)
    .agg({
        "Revenue":"sum",
        "Profit":"sum"
    })
)
#revenue
fig = px.bar(
    segment,
    x="Customer_Segment",
    y="Revenue",
    color="Revenue",
    title="Revenue by Customer Segment"
)

st.plotly_chart(fig, use_container_width=True)

# proit
fig = px.bar(
    segment,
    x="Customer_Segment",
    y="Profit",
    color="Profit",
    title="Profit by Customer Segment"
)

st.plotly_chart(fig, use_container_width=True)


#gender analysis
  # revenue
gender = (
    filtered_df
    .groupby("Customer_Gender", as_index=False)
    .agg({
        "Revenue":"sum",
        "Profit":"sum"
    })
)

#pie chart
fig = px.pie(
    gender,
    names="Customer_Gender",
    values="Revenue",
    title="Revenue Distribution by Gender"
)

st.plotly_chart(fig, use_container_width=True)

#profit
fig = px.pie(
    gender,
    names="Customer_Gender",
    values="Profit",
    title="Profit Distribution by Gender"
)

st.plotly_chart(fig, use_container_width=True)


## PAYMENT METHOS ANALYSIS
payment = (
    filtered_df
    .groupby("Payment_Method", as_index=False)
    .agg({
        "Revenue":"sum",
        "Profit":"sum"
    })
)
#revenue
fig = px.bar(
    payment,
    x="Payment_Method",
    y="Revenue",
    color="Revenue",
    title="Revenue by Payment Method"
)

st.plotly_chart(fig, use_container_width=True)

#profit
fig = px.bar(
    payment,
    x="Payment_Method",
    y="Profit",
    color="Profit",
    title="Profit by Payment Method"
)

st.plotly_chart(fig, use_container_width=True)

#SHIPPING METHOS ANALYSIS
shipping = (
    filtered_df
    .groupby("Shipping_Method", as_index=False)
    .agg({
        "Revenue":"sum",
        "Profit":"sum"
    })
)

fig = px.bar(
    shipping,
    x="Shipping_Method",
    y="Profit",
    color="Profit",
    title="Profit by Shipping Method"
)

st.plotly_chart(fig, use_container_width=True)

#ORDER STATUS
status = (
    filtered_df
    .groupby("Order_Status", as_index=False)
    .size()
)
fig = px.pie(
    status,
    names="Order_Status",
    values="size",
    title="Order Status Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# CUSTOMER SEGMENT TABLE
st.subheader("Customer Segment Summary")

st.dataframe(
    segment,
    use_container_width=True,
    hide_index=True
)

##AUTOMATIC BUSINESS INSIGHTS
st.subheader("💡 Customer Insights")

top_segment = (
    segment.sort_values(
        "Profit",
        ascending=False
    )
    .iloc[0]
)

best_payment = (
    payment.sort_values(
        "Profit",
        ascending=False
    )
    .iloc[0]
)

best_shipping = (
    shipping.sort_values(
        "Profit",
        ascending=False
    )
    .iloc[0]
)

st.success(f"""
### Key Insights

• The **{top_segment['Customer_Segment']}** segment generated the highest profit.

• **{best_payment['Payment_Method']}** is the most profitable payment method.

• **{best_shipping['Shipping_Method']}** produced the highest profit.

• Total customers analysed: **{customers:,}**.
""")

