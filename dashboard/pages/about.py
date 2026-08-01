import streamlit as st

#page configuration

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About This Project")

st.markdown("---")

##project overview

st.header("📌 Project Overview")

st.write("""
The **E-Commerce Country Profitability Prediction** project was developed to
help e-commerce businesses identify the factors that influence profitability
across different countries and predict the expected profit of future
transactions using machine learning.

The application combines exploratory data analysis, predictive modeling,
model interpretation, and interactive dashboards to support
data-driven business decision-making.
""")

##busim=ness problem

st.header("🎯 Business Problem")

st.write("""
E-commerce companies operate in multiple countries with different customer
behaviors, pricing strategies, logistics costs, and purchasing patterns.

Without predictive analytics, businesses may struggle to:

- Identify profitable markets.
- Optimize pricing strategies.
- Reduce unnecessary discounts.
- Improve inventory planning.
- Increase overall profitability.

This project addresses these challenges by predicting transaction profit
based on historical e-commerce data.
""")

##dataset description

st.header("📂 Dataset")

st.write("""
The dataset contains historical e-commerce transactions and includes
features describing products, customer purchases, pricing,
shipping, and profitability.

Key variables include:

- Country
- Season
- Category
- Sub-Category
- Product Name
- Unit Price
- Quantity
- Discount
- Shipping Cost
- Shipping Days
- Payment Method
- Profit (Target Variable)
""")

## machine learning workflow

st.header("🤖 Machine Learning Workflow")

st.write("""
The project followed a complete machine learning pipeline:

1. Data Cleaning
2. Exploratory Data Analysis (EDA)
3. Feature Engineering
4. Data Preprocessing
5. One-Hot Encoding
6. Model Training
7. Hyperparameter Tuning
8. Model Evaluation
9. SHAP Interpretation
10. Dashboard Deployment
""")

##models evaluated
st.header("📈 Machine Learning Models")

st.write("""
Several regression algorithms were trained and evaluated:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor

After hyperparameter tuning and evaluation,
the XGBoost model was selected as the final model due to
its strong predictive performance and interpretability.
""")

##technologies used

st.header("🛠 Technologies")

st.write("""
Programming Language

- Python

Machine Learning

- Scikit-learn
- XGBoost
- SHAP

Data Processing

- Pandas
- NumPy

Visualization

- Plotly
- Matplotlib

Dashboard

- Streamlit
""")

##business impact

st.header("💼 Business Impact")

st.write("""
The solution can support decision-makers by:

- Identifying high-profit countries.
- Understanding key drivers of profitability.
- Predicting profit before launching products.
- Optimizing pricing and discount strategies.
- Reducing operational costs.
- Supporting strategic expansion decisions.
""")

##duture improvement 
st.header("🚀 Future Improvements")

st.write("""
Potential enhancements include:

- Time-series profit forecasting.
- Customer segmentation.
- Real-time sales prediction.
- Live database integration.
- Cloud deployment.
- Automated model retraining.
- Interactive business recommendation engine.
""")

##
st.header("👨‍💻 About the Developer")

st.write("""
**Name:** Segun A.

**Role:** Data Scientist | Machine Learning Enthusiast

**Interests:**

- Machine Learning
- Artificial Intelligence
- Data Analytics
- Predictive Modeling
- Business Intelligence

This project demonstrates the practical application of machine
learning to solve real-world business problems.
""")

##contact indormation

st.header("📬 Contact")

st.write("""
GitHub:
https://github.com/DVictor101

LinkedIn:
https://www.linkedin.com/in/segunadedotun

Email:
seguntimileyin489@gmail.com
""")

##footer 

st.markdown("---")

st.caption(
    "© 2026 E-Commerce Country Profitability Prediction Dashboard | Built with Streamlit and Python"
)