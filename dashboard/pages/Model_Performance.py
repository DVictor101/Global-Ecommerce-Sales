import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Model Performance")

st.write("""
This page presents the performance of the final XGBoost model,
including evaluation metrics, feature importance and SHAP model interpretation.
""")

##
##load data
@st.cache_resource
def load_model():
    return joblib.load("models/profit_prediction_model.pkl")

model = load_model()

##load dataset
@st.cache_data
def load_data():
    return pd.read_csv("../data_folder/feature_engineerd_data.csv")


df = load_data()


##prepare data
X = df.drop(columns=["Profit"])

y = df["Profit"]

##split data
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=34
)

##predictions

predictions = model.predict(x_test)

##metrics
mae = mean_absolute_error(y_test, predictions)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

##kpi cards

col1, col2, col3 = st.columns(3)

col1.metric("MAE", f"{mae:.2f}")

col2.metric("RMSE", f"{rmse:.2f}")

col3.metric("R²", f"{r2:.3f}")

##actual vs predicted
st.subheader("Actual vs Predicted")

fig, ax = plt.subplots(figsize=(7,6))

ax.scatter(
    y_test,
    predictions,
    alpha=0.6
)

ax.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    linestyle="--"
)

ax.set_xlabel("Actual Profit")

ax.set_ylabel("Predicted Profit")

st.pyplot(fig)

#residual plot

st.subheader("Residual Plot")

residuals = y_test - predictions

fig, ax = plt.subplots(figsize=(7,6))

ax.scatter(
    predictions,
    residuals,
    alpha=0.6
)

ax.axhline(
    0,
    linestyle="--"
)

ax.set_xlabel("Predicted Profit")

ax.set_ylabel("Residuals")

st.pyplot(fig)

##feature importance

st.subheader("Feature Importance")

preprocessor = model.named_steps["Preprocessor"]

xgb = model.named_steps["model"]

feature_names = preprocessor.get_feature_names_out()

importance = pd.DataFrame({

    "Feature": feature_names,

    "Importance": xgb.feature_importances_

})

importance = importance.sort_values(
    "Importance",
    ascending=False
).head(20)

fig, ax = plt.subplots(figsize=(10,7))

ax.barh(
    importance["Feature"],
    importance["Importance"]
)

ax.invert_yaxis()

st.pyplot(fig)

##shap plot summary
st.subheader("SHAP Summary Plot")

#transform data
X_test_processed = preprocessor.transform(x_test)

##convert to dense
X_test_dense = X_test_processed.toarray()

##compute shap values
explainer = shap.TreeExplainer(xgb)

shap_values = explainer.shap_values(X_test_dense)

##create figure
fig, ax = plt.subplots(figsize=(10,7))

shap.summary_plot(

    shap_values,

    X_test_dense,

    feature_names=feature_names,

    show=False

)

st.pyplot(fig)

##shap bar plot
st.subheader("SHAP Feature Importance")
fig, ax = plt.subplots(figsize=(10,7))

shap.summary_plot(

    shap_values,

    X_test_dense,

    feature_names=feature_names,

    plot_type="bar",

    show=False

)

st.pyplot(fig)

##model interpretation
st.markdown("---")

st.subheader("Model Interpretation")

st.write("""

The tuned XGBoost model demonstrated strong predictive performance,
achieving a high coefficient of determination (R²) while maintaining
relatively low prediction errors.

Feature importance analysis identified Unit Price, Discount and
Quantity as the primary factors influencing profitability.

SHAP analysis further explains the contribution of each feature
to individual predictions, providing transparency and improving
trust in the machine learning model.

These insights enable businesses to optimize pricing strategies,
manage inventory effectively and prioritize high-performing markets.

""")

