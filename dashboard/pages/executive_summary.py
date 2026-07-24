import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

#load date
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_PATH = BASE_DIR / "data_folder" / "Feature_engineered_data.csv"

    df = pd.read_csv(DATA_PATH)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

#title
st.title("📑 Executive Summary")

st.markdown("""
A high-level summary of business performance, key insights, and strategic recommendations derived from historical data and predictive analytics.
""")
#overall kpi
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)
countries = df["Country"].nunique()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue > 0 else 0
)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Revenue", f"${total_revenue:,.0f}")
k2.metric("Profit", f"${total_profit:,.0f}")
k3.metric("Orders", f"{total_orders:,}")
k4.metric("Countries", countries)
k5.metric("Profit Margin", f"{profit_margin:.2f}%")

##calculate key insight
country_profit = (
    df.groupby("Country", as_index=False)["Profit"]
      .sum()
      .sort_values("Profit", ascending=False)
)

best_country = country_profit.iloc[0]

#best region
region_profit = (
    df.groupby("Region", as_index=False)["Profit"]
      .sum()
      .sort_values("Profit", ascending=False)
)

best_region = region_profit.iloc[0]

#best category
category_profit = (
    df.groupby("Category", as_index=False)["Profit"]
      .sum()
      .sort_values("Profit", ascending=False)
)

best_category = category_profit.iloc[0]

#best product
product_profit = (
    df.groupby("Product_Name", as_index=False)["Profit"]
      .sum()
      .sort_values("Profit", ascending=False)
)

best_product = product_profit.iloc[0]

#best customer segment
segment_profit = (
    df.groupby("Customer_Segment", as_index=False)["Profit"]
      .sum()
      .sort_values("Profit", ascending=False)
)

best_segment = segment_profit.iloc[0]

##EXECUTIVESUMMARY CARD
c1, c2 = st.columns(2)

with c1:

    st.success(f"""
### 🌍 Best Country

**{best_country['Country']}**

Profit:

${best_country['Profit']:,.0f}
""")

    st.success(f"""
### 🏆 Best Region

**{best_region['Region']}**

Profit:

${best_region['Profit']:,.0f}
""")

with c2:

    st.success(f"""
### 📦 Best Category

**{best_category['Category']}**

Profit:

${best_category['Profit']:,.0f}
""")

    st.success(f"""
### ⭐ Best Product

**{best_product['Product_Name']}**

Profit:

${best_product['Profit']:,.0f}
""")

#profit distribution
st.subheader("Profit by Country")

fig = px.bar(
    country_profit.head(10),
    x="Country",
    y="Profit",
    color="Profit",
    title="Top 10 Countries"
)

st.plotly_chart(fig, use_container_width=True)

#business recommendation
st.subheader("Strategic Recommendations")
st.info(f"""
### Expansion Strategy

The analysis indicates that **{best_country['Country']}** currently generates the highest total profit.

Recommended actions:

• Expand into **{best_country['Country']}** first.

• Focus investment on the **{best_category['Category']}** category.

• Prioritize **{best_product['Product_Name']}** in marketing campaigns.

• Target the **{best_segment['Customer_Segment']}** customer segment.

• Allocate additional inventory to high-performing markets while reviewing strategies for lower-performing countries.
""")


#business healtht score
score = 0

if profit_margin > 20:
    score += 40
elif profit_margin > 10:
    score += 25

if total_profit > 500000:
    score += 30
elif total_profit > 250000:
    score += 20

if countries >= 15:
    score += 30
elif countries >= 10:
    score += 20

st.subheader("Business Health Score")

st.progress(score / 100)

st.metric("Score", f"{score}/100")

#final executive conclusion
st.success(f"""
## Executive Conclusion

The business has generated **${total_revenue:,.0f}** in revenue and **${total_profit:,.0f}** in profit across **{countries}** countries.

Analysis identifies **{best_country['Country']}** as the strongest market based on profitability, with **{best_category['Category']}** emerging as the highest-performing category.

The **{best_segment['Customer_Segment']}** customer segment contributes the greatest share of profit, while **{best_product['Product_Name']}** is the top-performing product.

These findings support prioritizing expansion into **{best_country['Country']}**, increasing investment in **{best_category['Category']}**, and focusing marketing efforts on **{best_segment['Customer_Segment']}** customers.
""")