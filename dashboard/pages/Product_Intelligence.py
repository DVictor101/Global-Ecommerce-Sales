import streamlit as st
import pandas as pd
import plotly.express as px

#page configuration

st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
    layout="centered"
)

st.title("📦 Product Analysis")

st.markdown("""
This page provides detailed insights into product performance by analyzing
profitability, sales volume, discounts, and shipping costs across products
and categories.
""")

st.markdown("---")

#loading dataset
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


#category filter 

category = st.selectbox(
    "Select Product Category",
    sorted(df["Category"].unique())
)

category_df = df[df["Category"] == category]

#kpi cards 

total_profit = category_df["Profit"].sum()

average_profit = category_df["Profit"].mean()

total_quantity = category_df["Quantity"].sum()

products = category_df["Product_Name"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Profit", f"${total_profit:,.2f}")

col2.metric("📈 Average Profit", f"${average_profit:.2f}")

col3.metric("📦 Quantity Sold", f"{total_quantity:,}")

col4.metric("🛍 Products", products)

##profit subcategory

st.markdown("---")

st.subheader("Profit by Sub-Category")

subcategory_profit = (
    category_df
    .groupby("Sub_Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    subcategory_profit,
    x="Sub_Category",
    y="Profit",
    color="Profit",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

##top 10 most profitable product

st.markdown("---")

st.subheader("Top 10 Products")

top_products = (
    category_df
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

##bottom 10 products

st.markdown("---")

st.subheader("Bottom 10 Products")

bottom_products = (
    category_df
    .groupby("Product_Name")["Profit"]
    .sum()
    .sort_values()
    .head(10)
    .reset_index()
)

fig = px.bar(
    bottom_products,
    x="Profit",
    y="Product_Name",
    orientation="h",
    color="Profit",
    text_auto=".2s"
)

fig.update_layout(
    yaxis={"categoryorder": "total descending"}
)

st.plotly_chart(fig, use_container_width=True)

##discount by profit
st.markdown("---")

st.subheader("Discount vs Profit")

fig = px.scatter(
    category_df,
    x="Discount",
    y="Profit",
    color="Sub_Category",
    hover_name="Product_Name"
)

st.plotly_chart(fig, use_container_width=True)

## quantity vs profit


st.markdown("---")

st.subheader("Quantity Sold vs Profit")

fig = px.scatter(
    category_df,
    x="Quantity",
    y="Profit",
    color="Sub_Category",
    hover_name="Product_Name"
)

st.plotly_chart(fig, use_container_width=True)

##shipping vs cost

st.markdown("---")
st.subheader("Shipping Cost vs Profit")

fig = px.scatter(
    category_df,
    x="Shipping_Cost",
    y="Profit",
    color="Sub_Category",
    hover_name="Product_Name"
)

st.plotly_chart(fig, use_container_width=True)

##product summary table

st.markdown("---")

st.subheader("Product Summary")

summary = (
    category_df
    .groupby("Product_Name")
    .agg(
        Total_Profit=("Profit", "sum"),
        Average_Profit=("Profit", "mean"),
        Quantity=("Quantity", "sum"),
        Average_Discount=("Discount", "mean"),
        Average_Shipping_Cost=("Shipping_Cost", "mean")
    )
    .reset_index()
)

st.dataframe(summary, use_container_width=True)