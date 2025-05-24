import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def linear_regression_prediction(df_filtered):
    st.markdown("""
    ### 📈 What This Regression Section Does

    This section forecasts SU-related values using two types of regression models:

    - **Linear Regression**: Fits a straight line. Best for simple, steady trends.
    - **Polynomial Regression**: Fits a curve. Best when trends accelerate or bend.

    Choose a model type and a future year to see predictions for:
    - Total SU per student
    - Handicap allowance
    - Parental allowance

    The chart shows historical data, model prediction lines, and your selected year’s forecast.
    """)
    future_year = st.selectbox("Select prediction year (2025–2035):", list(range(2025, 2036)))

    model_type = st.selectbox("Choose regression model:", ["Linear", "Polynomial"])
    degree = 1

    for col, label, color in zip(
        ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger'],
        ['Total SU per student', 'Handicap tillæg', 'Forsørger tillæg'],
        ['teal', 'orange', 'purple']
    ):
        X = df_filtered[['Aar']].values
        y = df_filtered[col].values

        if model_type == "Polynomial":
            degree = st.slider(f"Select polynomial degree for {label}:", 2, 5, 2)
            poly = PolynomialFeatures(degree=degree)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            pred = model.predict(poly.transform([[future_year]]))[0]
            y_pred = model.predict(X_poly)
        else:
            model = LinearRegression()
            model.fit(X, y)
            pred = model.predict([[future_year]])[0]
            y_pred = model.predict(X)

        st.write(f"\n📈 Predicted {label} for {future_year}: {pred:,.0f} DKK")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(X.flatten(), y, color=color)
        ax.plot(X.flatten(), y_pred, linestyle='--', color='black')
        ax.scatter(future_year, pred, color='red', marker='X', s=100)
        ax.set_title(f"Prediction of {label} using {model_type} Regression")
        st.pyplot(fig)

def train_test_model_analysis(df):
    st.subheader("Train/Test Split and Model Accuracy")

    feature_cols = ['Aar', 'Antal_stoettemodtagere', 'Antal_handicap_tillaeg', 'Antal_forsorger_tillaeg']
    target_col = 'SU_pr_student'

    df_clean = df.dropna(subset=feature_cols + [target_col])
    X = df_clean[feature_cols]
    y = df_clean[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    st.write(f"R² Score: {r2_score(y_test, predictions):.4f}")
    st.write(f"Mean Squared Error (MSE): {mean_squared_error(y_test, predictions):,.0f}")

    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    st.write(f"Cross-validated R² (5-fold): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    residuals = y_test - predictions
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(predictions, residuals, alpha=0.7)
    ax.axhline(0, color='red', linestyle='--')
    ax.set_xlabel("Predicted Values")
    ax.set_ylabel("Residuals")
    ax.set_title("Residual Plot")
    st.pyplot(fig)

    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_
    }).sort_values(by='Coefficient', key=abs, ascending=False)
    st.subheader("Feature Importance (Linear Regression Coefficients)")
    st.dataframe(coef_df)

def compare_regression_models(df_filtered):
    st.subheader("📊 Compare Regression Models")
    st.markdown("""
    This chart compares **Linear** and **Polynomial (degrees 2 & 3)** regression fits  
    for each SU metric. It helps you see which model best matches the historical data.
    """)

    for col, label, color in zip(
        ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger'],
        ['Total SU per student', 'Handicap tillæg', 'Forsørger tillæg'],
        ['teal', 'orange', 'purple']
    ):
        X = df_filtered[['Aar']].values
        y = df_filtered[col].values

        X_range = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)

        # Linear
        lin_model = LinearRegression()
        lin_model.fit(X, y)
        y_pred_lin = lin_model.predict(X_range)

        # Polynomial deg 2
        poly2 = PolynomialFeatures(degree=2)
        X_poly2 = poly2.fit_transform(X)
        poly2_model = LinearRegression()
        poly2_model.fit(X_poly2, y)
        y_pred_poly2 = poly2_model.predict(poly2.transform(X_range))

        # Polynomial deg 3
        poly3 = PolynomialFeatures(degree=3)
        X_poly3 = poly3.fit_transform(X)
        poly3_model = LinearRegression()
        poly3_model.fit(X_poly3, y)
        y_pred_poly3 = poly3_model.predict(poly3.transform(X_range))

        # Plot
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(X, y, color=color, label="Actual", alpha=0.7)
        ax.plot(X_range, y_pred_lin, '--', label="Linear", color='black')
        ax.plot(X_range, y_pred_poly2, label="Polynomial (deg 2)", color='blue')
        ax.plot(X_range, y_pred_poly3, label="Polynomial (deg 3)", color='green')

        ax.set_title(f"Model Comparison: {label}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Amount (DKK)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
