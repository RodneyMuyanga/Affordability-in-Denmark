import streamlit as st

def show_salary_agenda():
    st.subheader("🗂️ Agenda for Presentation")

    st.markdown("""
    This presentation will walk you through an end-to-end Business Intelligence analysis focused on the development of wages in Denmark over the last decade, in relation to inflation.

    **Here's what we’ll cover:**

    1. **Data Preparation** – Cleaning and preparing salary data from 2013 to 2023.
    2. **Statistical Analysis** – Understanding distributions, outliers, and correlations.
    3. **Salary Development Over Time** – Trends and sector breakdowns.
    4. **Inflation Forecast** – Predicting future affordability based on wage and price trends.
    5. **Conclusion** – Summary of insights and policy implications.

    """)

    st.markdown("---")
    st.markdown("### 📋 Agenda Overview with Curriculum Mapping")

    st.markdown("""
    | Tab                     | Content                                                | Curriculum Coverage                                      |
    |-------------------------|---------------------------------------------------------|-----------------------------------------------------------|
    | **Agenda**              | Overview, purpose, problem definition                  | Report design, problem formulation                        |
    | **Data preparation**    | ETL: loading, cleaning, structuring                    | Data Ingestion & Cleaning                                 |
    | **Salary development**  | Visual trends in salary over time                      | Visualisation, bar/line charts                           |
    | **Statistical Analysis**| Stats, outliers, ML regression + classification        | Statistics, ML, visualisation, z-score, regression        |
    | **Inflation forecast**  | Compare wages and inflation, ML-forecast, clustering   | Forecasting, clustering, ML evaluation, visualisation     |
    | **Conclusion**          | Results, reflections, perspectives                     | Reporting & communication                                 |
    """)
