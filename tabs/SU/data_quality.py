import streamlit as st
import pandas as pd
from .data_loading import remove_outliers

def analyze_missing_values(df):
    missing_summary = df.isnull().sum()
    missing_percent = (missing_summary / len(df)) * 100
    return pd.DataFrame({'Missing Values': missing_summary, 'Percent': missing_percent})

def show_data_quality_checks(df):
    if st.checkbox("Show missing value analysis"):
        st.subheader("Missing Value Summary")
        st.dataframe(analyze_missing_values(df))
    if st.checkbox("Remove outliers (Z-score method)"):
        cols = ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']
        df = remove_outliers(df, cols)
        st.success("Outliers removed.")
    return df
