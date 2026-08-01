
import plotly
import streamlit as st
import pandas as pd
import joblib
forecast = pd.read_csv(
    "../data_folder/Profit_Forecast.csv"
)
model = joblib.load(
    "../models/profit_prediction_model.pkl"
)

st.selectbox("Country", ...)
st.selectbox("Category", ...)
st.number_input("Quantity")
st.number_input("Discount")

st.success("model loaded succesfully!")

