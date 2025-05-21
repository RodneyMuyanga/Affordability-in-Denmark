import streamlit as st

def show_salary_forecast():
    st.subheader("🔮 Forecasting inflation")

    st.markdown("""
    In this section, we look ahead and try to estimate how inflation – and thus real wages – may develop in the coming years.

    Future versions may include:
    - Forecast models such as Prophet or ARIMA
    - Simulated inflation scenarios
    - Comparison with historical salary trends

    📌 Example: If inflation stays at 4% while salary only rises by 2%, purchasing power is lost.
    """)
