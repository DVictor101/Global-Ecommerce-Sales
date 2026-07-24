import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "profit_prediction_model.pkl"

model = joblib.load(MODEL_PATH)
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data_folder" / "Feature_engineered_data.csv"

    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()

st.title("🤖 AI Profit Prediction")

st.markdown("""
Predict the expected profit for a future order based on
business characteristics.
""")

#user inputs

#season
season = st.selectbox(
    "Season",
    sorted(df["Season"].unique())
)

#region
region = st.selectbox(
    "Region",
    sorted(df["Region"].unique())
)

#country
country = st.selectbox(
    "Country",
    sorted(df["Country"].unique())
)

#category
category = st.selectbox(
    "Category",
    sorted(df["Category"].unique())
)

#subcategory
subcategory = st.selectbox(
    "Sub Category",
    sorted(df["Sub_Category"].unique())
)

# Product Name
product_name = st.selectbox(
    "Product Name",
    sorted(df["Product_Name"].unique())
)

#unit price
unit_price = st.number_input(
    "Unit Price",
    min_value=1.0,
    value=100.0
)


#quantity]
quantity = st.number_input(
    "Quantity",
    min_value=1,
    value=5
)


#discount
discount = st.slider(
    "Discount (%)",
    0,
    50,
    10
)

#shipping cost
shipping_cost = st.number_input(
    "Shipping Cost",
    min_value=0.0,
    value=20.0
)

# Shipping Method
shipping_method = st.selectbox(
    "Shipping Method",
    sorted(df["Shipping_Method"].unique())
)

#shipping days
shipping_days = st.slider(
    "Shipping Days",
    1,
    20,
    5
)

# Payment Method
payment_method = st.selectbox(
    "Payment Method",
    sorted(df["Payment_Method"].unique())
)

# prediction data
input_df = pd.DataFrame({
    "Country": [country],
    "Region": [region],
    "Category": [category],
    "Sub_Category": [subcategory],
    "Product_Name": [product_name],
    "Season": [season],
    "Shipping_Method": [shipping_method],
    "Payment_Method": [payment_method],
    "Quantity": [quantity],
    "Unit_Price": [unit_price],
    "Discount": [discount],
    "Shipping_Cost": [shipping_cost],
    "Shipping_Days": [shipping_days]
})




#prediction
if st.button("Predict Profit"):
   

    prediction = model.predict(input_df)

    st.success(f"Predicted Profit: ${prediction[0]:,.2f}")

    # 👉 Move logic INSIDE here
    if prediction[0] > 500:

        st.success("""
### Excellent Opportunity

This configuration is expected to generate a high profit.
It is a strong candidate for expansion.
""")

    elif prediction[0] > 250:

        st.info("""
### Moderate Opportunity

The expected profit is positive but there may be room for improvement through pricing, discounts, or logistics.
""")

    else:

        st.warning("""
### Low Opportunity

The predicted profit is relatively low. Consider reviewing pricing, costs, or market selection before expanding.
""")
print(model.feature_names_in_)