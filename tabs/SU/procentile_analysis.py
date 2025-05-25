import streamlit as st
import pandas as pd
import numpy as np

def show_percentile_analysis(df):
    st.markdown("""
    ### 📊 Percentile Rank of SU per Student

    Since classification didn't provide value due to limited data and a naturally continuous target, we now show **percentile ranks** instead:

    > "How does SU per student this year compare to other years?"

    This helps identify whether a year's support level is relatively low, average, or high.
    """)

    if 'SU_pr_student' not in df.columns or 'Aar' not in df.columns:
        st.warning("Required columns missing: 'SU_pr_student' and 'Aar'")
        return

    # missing values in SU column
    df = df.dropna(subset=['SU_pr_student'])

    # percentile rank
    df['Percentile'] = df['SU_pr_student'].rank(pct=True) * 100

    # format columns
    df_percentiles = df[['Aar', 'SU_pr_student', 'Percentile']].sort_values('Aar')
    df_percentiles['Aar'] = df_percentiles['Aar'].astype(int).astype(str)
    df_percentiles['SU_pr_student'] = df_percentiles['SU_pr_student'].round(0).astype(int)
    df_percentiles['Percentile'] = df_percentiles['Percentile'].round(1)

    # table
    st.dataframe(df_percentiles.rename(columns={
        'Aar': 'Year',
        'SU_pr_student': 'SU per Student (DKK)',
        'Percentile': 'Percentile Rank (%)'
    }))

    st.markdown("""
    **Interpretation:**
    - Percentile 95% → Among the highest support years
    - Percentile 50% → Around the median year
    - Percentile 10% → One of the lowest support years
    """)
