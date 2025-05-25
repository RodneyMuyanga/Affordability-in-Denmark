import streamlit as st
import pandas as pd
import numpy as np
from .data_loading import remove_outliers

def analyze_missing_values(df):
    missing_summary = df.isnull().sum()
    missing_percent = (missing_summary / len(df)) * 100
    return pd.DataFrame({
        'Missing Values': missing_summary,
        'Missing %': missing_percent
    }).sort_values(by='Missing Values', ascending=False)

def impute_selected_columns(df, cols, method='mean'):
    df = df.copy()
    for col in cols:
        if method == 'mean':
            df[col] = df[col].fillna(df[col].mean())
        elif method == 'median':
            df[col] = df[col].fillna(df[col].median())
        elif method == 'interpolate':
            df[col] = df[col].interpolate()
    return df

def clean_dataframe(df, required_cols):
    return df.dropna(subset=required_cols)

def show_data_quality_checks(df):
    st.subheader("🧹 Data Cleaning & Quality Check")

    if st.checkbox("🔍 Show missing value summary"):
        st.dataframe(analyze_missing_values(df))

    # Choose columns to clean
    important_cols = ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger', 'Aar']

    # Outlier removal
    if st.checkbox("❌ Remove outliers using Z-score (only affects key columns)"):
        df = remove_outliers(df, important_cols, z_thresh=3)
        st.success("Outliers removed based on Z-score threshold.")

    # Missing value handling
    st.markdown("**Handle Missing Values**")
    impute_option = st.radio(
        "Choose a method to handle missing data in key columns:",
        options=["None", "Interpolate (recommended)", "Mean Imputation", "Median Imputation", "Drop Rows with Missing"],
        help="This only applies to selected key columns, not the whole dataset."
    )

    if impute_option == "Interpolate (recommended)":
        df = impute_selected_columns(df, important_cols, method='interpolate')
        st.success("Missing values filled using interpolation.")
    elif impute_option == "Mean Imputation":
        df = impute_selected_columns(df, important_cols, method='mean')
        st.success("Missing values filled using mean.")
    elif impute_option == "Median Imputation":
        df = impute_selected_columns(df, important_cols, method='median')
        st.success("Missing values filled using median.")
    elif impute_option == "Drop Rows with Missing":
        df = clean_dataframe(df, important_cols)
        st.success("Rows with missing values in key columns dropped.")

    return df
