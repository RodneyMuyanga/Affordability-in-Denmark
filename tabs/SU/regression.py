import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def linear_regression_prediction(df_filtered):
    future_year = st.selectbox("Select prediction year (2025–2035):", list(range(2025, 2036)))

    for col, label, color in zip(
        ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger'],
        ['Total SU per student', 'Handicap tillæg', 'Forsørger tillæg'],
        ['teal', 'orange', 'purple']
    ):
        X = df_filtered['Aar'].values.reshape(-1, 1)
        y = df_filtered[col].values

        model = LinearRegression()
        model.fit(X, y)
        pred = model.predict(np.array([[future_year]]))[0]

        st.write(f"📈 Predicted {label} for {future_year}: {pred:,.0f} DKK")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(df_filtered['Aar'], y, color=color)
        ax.plot(df_filtered['Aar'], model.predict(X), linestyle='--', color='black')
        ax.scatter(future_year, pred, color='red', marker='X', s=100)
        ax.set_title(f"Prediction of {label}")
        st.pyplot(fig)

def train_test_model_analysis(df):
    st.subheader("Train/Test Split and Model Accuracy")

    # Selecting features and target — example using these SU columns and year
    feature_cols = ['Aar', 'Antal_stoettemodtagere', 'Antal_handicap_tillaeg', 'Antal_forsorger_tillaeg']
    target_col = 'SU_pr_student'

    # Clean dataset for NaNs in features or target
    df_clean = df.dropna(subset=feature_cols + [target_col])
    X = df_clean[feature_cols]
    y = df_clean[target_col]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    st.write(f"R² Score: {r2_score(y_test, predictions):.4f}")
    st.write(f"Mean Squared Error (MSE): {mean_squared_error(y_test, predictions):,.0f}")

    # Residual plot
    residuals = y_test - predictions
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(predictions, residuals, alpha=0.7)
    ax.axhline(0, color='red', linestyle='--')
    ax.set_xlabel("Predicted Values")
    ax.set_ylabel("Residuals")
    ax.set_title("Residual Plot")
    st.pyplot(fig)

    # Feature importance using coefficients
    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_
    }).sort_values(by='Coefficient', key=abs, ascending=False)
    st.subheader("Feature Importance (Linear Regression Coefficients)")
    st.dataframe(coef_df)

