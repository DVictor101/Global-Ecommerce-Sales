import streamlit as st
import pandas as pd
import plotly.express as px

#data
@st.cache_data
def load_data():
    df = pd.read_csv("../data_folder/Feature_engineered_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

#title
st.title("📦 Product Intelligence")

st.markdown("""
Analyze product performance to identify the products and categories
that drive revenue and profitability.
""")

#sidebar
country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["Country"].unique())
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique())
)

subcategory = st.sidebar.selectbox(
    "Sub Category",
    ["All"] + sorted(df["Sub_Category"].unique())
)

#filters
filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == country
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if subcategory != "All":
    filtered_df = filtered_df[
        filtered_df["Sub_Category"] == subcategory
    ]

# product kpi

total_products = filtered_df["Product_Name"].nunique()

total_revenue = filtered_df["Revenue"].sum()

total_profit = filtered_df["Profit"].sum()

average_profit = filtered_df["Profit"].mean()

k1, k2, k3, k4 = st.columns(4)

k1.metric("Products", total_products)

k2.metric("Revenue", f"${total_revenue:,.0f}")

k3.metric("Profit", f"${total_profit:,.0f}")

k4.metric("Avg Profit / Order", f"${average_profit:,.2f}")


#top 10 products
top_products = (
    filtered_df
    .groupby("Product_Name", as_index=False)
    .agg({
        "Revenue": "sum",
        "Profit": "sum"
    })
    .sort_values("Profit", ascending=False)
    .head(10)
)

fig = px.bar(
    top_products,
    x="Profit",
    y="Product_Name",
    orientation="h",
    color="Profit",
    text_auto=".2s",
    title="Top 10 Products by Profit"
)

fig.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig, use_container_width=True)

# bottom 10product
bottom_products = (
    filtered_df
    .groupby("Product_Name", as_index=False)
    .agg({
        "Revenue": "sum",
        "Profit": "sum"
    })
    .sort_values("Profit")
    .head(10)
)

fig = px.bar(
    bottom_products,
    x="Profit",
    y="Product_Name",
    orientation="h",
    color="Profit",
    text_auto=".2s",
    title="Bottom 10 Products by Profit"
)

fig.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig, use_container_width=True)

## category performance 
category_summary = (
    filtered_df
    .groupby("Category", as_index=False)
    .agg({
        "Revenue": "sum",
        "Profit": "sum"
    })
)

#revenue
fig = px.bar(
    category_summary,
    x="Category",
    y="Revenue",
    color="Revenue",
    title="Revenue by Category"
)

st.plotly_chart(fig, use_container_width=True)

#profit
fig = px.bar(
    category_summary,
    x="Category",
    y="Profit",
    color="Profit",
    title="Profit by Category"
)

st.plotly_chart(fig, use_container_width=True)

##subcategory performance
subcategory_summary = (
    filtered_df
    .groupby("Sub_Category", as_index=False)
    .agg({
        "Revenue": "sum",
        "Profit": "sum"
    })
    .sort_values("Profit", ascending=False)
)

fig = px.bar(
    subcategory_summary,
    x="Sub_Category",
    y="Profit",
    color="Profit",
    title="Profit by Sub-Category"
)

st.plotly_chart(fig, use_container_width=True)

#revenue by profit

scatter_data = (
    filtered_df
    .groupby("Product_Name", as_index=False)
    .agg({
        "Revenue": "sum",
        "Profit": "sum"
    })
)

fig = px.scatter(
    scatter_data,
    x="Revenue",
    y="Profit",
    size="Revenue",
    color="Profit",
    hover_name="Product_Name",
    title="Revenue vs Profit by Product"
)

st.plotly_chart(fig, use_container_width=True)

#product summary table
product_summary = (
    filtered_df
    .groupby("Product_Name", as_index=False)
    .agg({
        "Revenue": "sum",
        "Profit": "sum",
        "Quantity": "sum"
    })
    .sort_values("Profit", ascending=False)
)

st.subheader("📋 Product Summary")

st.dataframe(
    product_summary,
    use_container_width=True,
    hide_index=True
)


#BUSINESS RECOMMENDATION
best_product = product_summary.iloc[0]
worst_product = product_summary.iloc[-1]

best_category = (
    category_summary
    .sort_values("Profit", ascending=False)
    .iloc[0]
)

st.success(f"""
## Product Insights

🏆 Best Product: **{best_product['Product_Name']}**

💰 Total Profit: **${best_product['Profit']:,.0f}**

📦 Best Category: **{best_category['Category']}**

📉 Lowest Performing Product: **{worst_product['Product_Name']}**

### Recommendation

Increase inventory and marketing for **{best_product['Product_Name']}** and focus investment on the **{best_category['Category']}** category. Review pricing, promotions, or demand for **{worst_product['Product_Name']}** to improve its performance or consider reducing investment.
""")
