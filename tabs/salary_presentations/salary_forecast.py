import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# -------------------------------------
# Load salary data from Excel
# -------------------------------------
def load_salary_data(group, year, wage_category):
    base_dir = "Data/Salary"
    if group == "All":
        folder = "Stats all 13 - 23 salary"
        prefix = "all"
    elif group == "Men":
        folder = "Stats All men 13 - 23 salary"
        prefix = "men"
    else:
        folder = "Stats All women 13 - 23 salary"
        prefix = "women"

    file_path = os.path.join(base_dir, folder, f"{prefix} {year}.xlsx")
    if not os.path.exists(file_path):
        return None, f"❌ File not found: {file_path}"

    try:
        df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")
        match_row = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(wage_category.lower()).any(), axis=1)]
        if match_row.empty:
            return None, f"⚠️ Wage category '{wage_category}' not found in {year}"
        row = match_row.iloc[0]
        values = row[3:8]
        values_numeric = pd.to_numeric(values, errors="coerce")
        if values_numeric.isnull().any():
            return None, "❌ Invalid values in salary data"
        return pd.DataFrame({"Hourly Wage (DKK)": values_numeric}), None
    except Exception as e:
        return None, f"❌ Error: {e}"

# -------------------------------------
# Show salary and inflation with forecast
# -------------------------------------
def show_salary_forecast():
    st.subheader("Salary Forecast and Inflation")

    years = list(range(2013, 2024))
    wages = []
    valid_years = []
    for year in years:
        df, err = load_salary_data("All", str(year), "STANDARDBEREGNET TIMEFORTJENESTE")
        if err or df is None:
            continue
        mean_wage = df["Hourly Wage (DKK)"].mean()
        wages.append(round(mean_wage, 1))
        valid_years.append(year)

    years = np.array(valid_years)
    wages = np.array(wages)
    inflation_rates = np.array([0.8, 0.6, 0.5, 0.3, 1.1, 0.7, 0.7, 0.3, 1.9, 8.5, 4.1])[-len(wages):]

    # Historical trends
    st.markdown("### 📈 Historical Salary and Inflation Trends")
    fig1, ax1 = plt.subplots()
    ax1.plot(years, wages, 'o-', label="Average Hourly Wage (DKK)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Hourly Wage (DKK)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(years, inflation_rates, 's--', color='red', label="Inflation (%)")
    ax2.set_ylabel("Inflation (%)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    fig1.legend(loc="upper left")
    st.pyplot(fig1)

    with st.expander("📌 Why did inflation spike in 2021?"):
        st.markdown("""
        Inflation in 2021 and 2022 rose sharply due to global disruptions:

        - Reopening after the COVID-19 pandemic  
        - Supply chain issues and rising energy prices  
        - High demand and government stimulus packages  

        These factors pushed inflation to its highest level in decades.
        """)

    # Real wages
    real_wages = wages / (1 + inflation_rates / 100)
    st.markdown("### 💰 Real Wage (Inflation-Adjusted)")
    fig2, ax = plt.subplots()
    ax.plot(years, real_wages, 'g^-', label="Real Hourly Wage (DKK)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Real Hourly Wage (DKK)")
    ax.set_title("Development of Real Wage Over Time")
    ax.legend()
    st.pyplot(fig2)

    # Combined plot
    st.markdown("### 📉 Real Wage vs. Inflation")
    fig3, ax1 = plt.subplots()
    ax1.plot(years, real_wages, 'g^-', label="Real Hourly Wage (DKK)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Real Wage (DKK)", color='green')
    ax1.tick_params(axis='y', labelcolor='green')

    ax2 = ax1.twinx()
    ax2.plot(years, inflation_rates, 'rs--', label="Inflation (%)")
    ax2.set_ylabel("Inflation (%)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    fig3.legend(loc="upper left")
    st.pyplot(fig3)

    with st.expander("📉 How does inflation affect wage increases?"):
        st.markdown("""
        When inflation rises faster than wages, **real purchasing power** decreases.  
        This is clearly seen in 2021, where **inflation spiked**, yet **real wages dropped** despite higher nominal pay.

        👉 Wages go up – but you can buy less with them.
        """)

    # Linear forecast
    X_years = years.reshape(-1, 1)
    model_wage = LinearRegression().fit(X_years, wages)
    future_years = np.arange(2024, 2034).reshape(-1, 1)
    predicted_wages = model_wage.predict(future_years)

    model_inflation = LinearRegression().fit(X_years, inflation_rates)
    predicted_inflation = model_inflation.predict(future_years)
    real_predicted_wages = predicted_wages / (1 + predicted_inflation / 100)

    st.markdown("### 📊 Predicted Real Hourly Wage")
    fig4, ax = plt.subplots()
    ax.plot(future_years, predicted_wages, 'b-', label="Predicted Nominal Wage")
    ax.plot(future_years, real_predicted_wages, 'g--', label="Predicted Real Wage")
    ax.set_xlabel("Year")
    ax.set_ylabel("Hourly Wage (DKK)")
    ax.set_title("Forecast: Nominal vs. Real Wage")
    ax.legend()
    st.pyplot(fig4)

    with st.expander("📊 What’s the difference between nominal and real wage?"):
        st.markdown("""
        **Nominal wage** (blue) shows expected earnings without adjusting for inflation.  
        **Real wage** (green) shows what the wage is truly worth — adjusted for inflation.

        👉 Even if pay rises, real value may grow slower if inflation is high.
        """)

    # Polynomial regression
    st.markdown("### 📐 Advanced Forecasting with Polynomial Regression")
    poly_model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
    poly_model.fit(X_years, wages)
    pred_poly = poly_model.predict(future_years)

    fig5, ax = plt.subplots()
    ax.plot(years, wages, 'ko-', label="Historical Wage")
    ax.plot(future_years, pred_poly, 'b--', label="Polynomial Regression Forecast")
    ax.set_xlabel("Year")
    ax.set_ylabel("Hourly Wage (DKK)")
    ax.set_title("Polynomial Regression: Wage Forecast")
    ax.legend()
    st.pyplot(fig5)

    with st.expander("📐 Why use Polynomial Regression?"):
        st.markdown("""
        Polynomial Regression captures wage trends and extends a curved trend line into the future.

        👉 Suitable for modeling growth over time — unlike simpler models that assume steady changes.
        """)

    st.success("✅ The analysis shows both historical wage trends and a reasonable forecast based on wage and inflation.")
