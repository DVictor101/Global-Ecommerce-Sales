import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet

#data
@st.cache_data
def load_data():
    df = pd.read_csv("../data_folder/Feature_engineered_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

#title
st.title("📈 Revenue & Profit Forecasting")

st.markdown("""
Forecast future business performance using Facebook Prophet.
""")


#choose forcast
forecast_type = st.selectbox(
    "Forecast",
    [
        "Revenue",
        "Profit"
    ]
)

#forecast horizon
months = st.slider(
    "Months to Forecast",
    3,
    24,
    12
)

#if revenue
if forecast_type == "Revenue":

    forecast_df = (
        df
        .groupby("Order_Date", as_index=False)["Revenue"]
        .sum()
    )

    forecast_df.columns = ["ds","y"]

#if profit
else:

    forecast_df = (
        df
        .groupby("Order_Date", as_index=False)["Profit"]
        .sum()
    )

    forecast_df.columns = ["ds","y"]

#train prophet
model = Prophet()

model.fit(forecast_df)

#create future dates
future = model.make_future_dataframe(
    periods=months,
    freq="M"
)

#predict
forecast = model.predict(future)

#forecast chart

fig = px.line(
    forecast,
    x="ds",
    y="yhat",
    title=f"{forecast_type} Forecast"
)

fig.add_scatter(
    x=forecast_df["ds"],
    y=forecast_df["y"],
    mode="lines",
    name="Historical"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#firecast tabkes
st.subheader("Forecast Results")

st.dataframe(
    forecast[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].tail(months),
    use_container_width=True
)

#business recommendation
future_prediction = forecast["yhat"].iloc[-1]
current = forecast_df["y"].iloc[-1]

if future_prediction > current:

    st.success(
        f"""
### Growth Expected 📈

Forecast suggests that **{forecast_type.lower()}**
will increase over the next
{months} months.
"""
    )

else:

    st.warning(
        f"""
### Decline Expected 📉

Forecast suggests a decrease in
future {forecast_type.lower()}.
"""
    )


