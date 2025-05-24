import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def show_salary_forecast():
    st.subheader("🔮 Salary Forecasting & Machine Learning Concepts")

    st.markdown("""
    This section demonstrates how salaries may develop in the future using regression techniques,
    and presents key machine learning concepts related to prediction and pattern discovery.
    """)

    # --- Simulated data (example from past years) ---
    years = np.array([2013, 2016, 2020, 2023]).reshape(-1, 1)
    wages = np.array([240, 255, 270, 296])  # Average hourly wages

    # --- Linear Regression Forecast ---
    model = LinearRegression().fit(years, wages)
    future_years = np.array(range(2024, 2034)).reshape(-1, 1)
    predicted_wages = model.predict(future_years)

    st.markdown("### 📈 Linear Regression Forecast: 2024–2033")
    fig1, ax1 = plt.subplots()
    ax1.plot(years.flatten(), wages, 'o-', label="Historical data")
    ax1.plot(future_years.flatten(), predicted_wages, 'r--', label="Forecast")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Hourly wage (DKK)")
    ax1.set_title("Forecast of Hourly Wages Based on Historical Trend")
    ax1.legend()
    st.pyplot(fig1)

    # --- Multiple Regression Explanation ---
    st.markdown("### 📊 Multiple Linear Regression (Concept)")
    st.markdown("""
    Multiple Linear Regression allows prediction based on multiple features, such as:
    - Year
    - Gender (e.g., 0 = Female, 1 = Male)
    - Sector (one-hot encoded)

    Example use case:
    ```python
    model = LinearRegression().fit(X, y)
    predicted_salary = model.predict(new_input)
    ```

    This model improves accuracy by considering multiple real-world factors.
    """)

    # --- ML Concepts ---
    st.markdown("### 🤖 Supervised vs. Unsupervised Learning")

    st.markdown("""
    **Supervised Learning**
    - Trains on known inputs and outputs
    - Used for:
        - Regression (predict salary)
        - Classification (e.g. classify high/low earners)

    **Unsupervised Learning**
    - Finds structure in unlabeled data
    - Used for:
        - Clustering employees by salary patterns
        - Dimensionality reduction (PCA)

    ✅ In this project:
    - Regression = Supervised
    - Clustering (e.g., KMeans) = Unsupervised
    """)

    st.success("Linear regression is used for forecasting. You can later expand with multiple regression or clustering.")
