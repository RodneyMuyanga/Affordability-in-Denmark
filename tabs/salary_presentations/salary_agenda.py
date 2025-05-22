import streamlit as st

def show_salary_agenda():
    st.subheader("🗂️ Agenda for Presentation")

    st.markdown("""
    This presentation will walk you through an end-to-end Business Intelligence analysis focused on the development of wages in Denmark over the last decade, in relation to inflation.

    **Here's what we’ll cover:**
    
    1. **Purpose and Motivation** – Why focus on salary and inflation?
    2. **Data Preparation** – Cleaning and preparing salary data from 2013 to 2023.
    3. **Statistical Analysis** – Understanding distributions, outliers, and correlations.
    4. **Salary Development Over Time** – Trends and sector breakdowns.
    5. **Inflation Forecast** – Predicting future affordability based on wage and price trends.
    6. **Conclusion** – Summary of insights and policy implications.

    ➡️ Use the top menu to follow along each step of the analysis.
    """)
