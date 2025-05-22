import pandas as pd
import streamlit as st

def show_conclusions():

    st.header("🔎 Conclusions & Methodology")
    st.markdown("""
    **Purpose:**  
    We set out to uncover how food prices have evolved in Denmark from 2014 to 2024 and to identify which categories experienced the most instability.

    **Methodological choices:**  
    - **Category Trend:** Line charts per category to track year-over-year changes.  
    - **Overall Trend:** Average across all categories to answer the question “Have prices generally gone up or down?”  
    - **Volatility:** Annual standard deviation to measure the dispersion of price changes.  
    - **Cluster Analysis:** K-means clustering to classify categories as “stable” versus “volatile.”  
    - **Comparison:** Selected key categories (bread, milk, vegetables) on the same axis to highlight differing dynamics.

    **Key findings:**  
    1. **Bread & cereal products** saw the largest spikes during the 2022–2023 inflationary peak.  
    2. **Milk & dairy** exhibited larger year-to-year swings, while **vegetables** were the most volatile overall.  
    3. The **overall average** hovered at or below 0% until 2021, then jumped sharply above 0% in 2022–2023.  
    4. **Volatility** also peaked in this period, confirming external shock effects from COVID, raw-material price surges, and energy costs.

    **Implications:**  
    - For **households**, this period of rapid price increases led to heightened budgeting uncertainty.  
    - For **policy-makers** and **retailers**, these insights suggest the need for targeted support measures during extreme price fluctuations.  
    """)
