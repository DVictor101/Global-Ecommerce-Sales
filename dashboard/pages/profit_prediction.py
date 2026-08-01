import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


#page configuration

st.set_page_config(
    page_title="Profit Prediction",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Profit Prediction")

st.markdown("""
Use the trained XGBoost model to estimate the expected profit for a new
e-commerce transaction.
""")

st.markdown("---")

##loadin the dataset

@st.cache_resource
def load_model():
    BASE_DIR = Path(__file__).resolve().parent.parent

    MODEL_PATH = BASE_DIR / "models" / "profit_prediction_model.pkl"

    st.write("BASE_DIR:", BASE_DIR)
    st.write("MODEL_PATH:", MODEL_PATH)
    st.write("Exists:", MODEL_PATH.exists())

    if not MODEL_PATH.exists():
        st.error(f"Model not found:\n{MODEL_PATH}")
        st.stop()

    return joblib.load(MODEL_PATH)

model = load_model()


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

##building input form
st.subheader("Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:

    season = st.selectbox(
        "Season",
        sorted(df["Season"].unique())
    )

    country = st.selectbox(
        "Country",
        sorted(df["Country"].unique())
    )

    category = st.selectbox(
        "Category",
        sorted(df["Category"].unique())
    )

    sub_category = st.selectbox(
        "Sub Category",
        sorted(df["Sub_Category"].unique())
    )

    product = st.selectbox(
        "Product Name",
        sorted(df["Product_Name"].unique())
    )


with col2:

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.0,
        value=100.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    discount = st.number_input(
        "Discount (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0
    )

    shipping_cost = st.number_input(
        "Shipping Cost",
        min_value=0.0,
        value=10.0
    )

    shipping_days = st.number_input(
        "Shipping Days",
        min_value=1,
        value=5
    )

    payment_method = st.selectbox(
        "Payment Method",
        sorted(df["Payment_Method"].unique())
    )

    ##prediction button

    predict = st.button("Predict Profit")

    ##preparing input
    if predict:
        new_data = pd.DataFrame({

        "Season":[season],
        "Country":[country],
        "Category":[category],
        "Sub_Category":[sub_category],
        "Product_Name":[product],
        "Unit_Price":[unit_price],
        "Quantity":[quantity],
        "Discount":[discount],
        "Shipping_Cost":[shipping_cost],
        "Shipping_Days":[shipping_days],
        "Payment_Method":[payment_method]

    })
        prediction = model.predict(new_data)[0]
        st.markdown("---")
        st.subheader("Prediction")
        st.success(
            f"Predicted Profit: ${prediction:,.2f}"
            )

        #probability rating
        if prediction > 400:
            st.success("🟢 High Profitability")
        elif prediction > 150:
            st.warning("🟡 Moderate Profitability")
        else:
            st.error("🔴 Low Profitability")
            #display input summary
            st.markdown("---")
            st.subheader("Transaction Summary")
            st.dataframe(new_data)
            ## add prediction tips
            st.markdown("---")
            st.info("""Tips for improving profitability:
            Increase sales quantity.
            Avoid excessive discounts.
            Focus on profitable countries.
            Reduce shipping costs where possible.
            Prioritize high-performing products.
            """)


#display prediction
   

    