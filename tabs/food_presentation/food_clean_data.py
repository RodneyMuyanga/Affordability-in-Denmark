import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

def load_and_clean():

# --- FILE PATH ---
    file_path = "Data/Food/FoodPricesComparedToPreviousYear.xlsx"

    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        st.stop()

    # --- LOAD HEADERS ---
    temp = pd.read_excel(file_path, header=None)
    years = temp.iloc[2, 2:].tolist()

    # --- DATA LOADING ---
    raw = pd.read_excel(file_path, skiprows=3, header=None)

    # Extract and clean
    data = raw.iloc[:, 1:].copy()

    # Check if number of year labels matches number of columns
    if len(years) == data.shape[1] - 1:
        data.columns = ['Category'] + years
    else:
        st.error(f"Mismatch in columns: Data has {data.shape[1]} columns, but only {len(years)} year labels.")
        st.stop()
    # Ensure 'Category' is string and rest are numeric
    data['Category'] = data['Category'].astype(str)

    # Clean common problematic characters before converting to numeric
    data.replace(["–", "—", "", " ", ".."], pd.NA, inplace=True)

    # Convert all year columns to numeric format
    for col in data.columns[1:]:
     data[col] = pd.to_numeric(data[col], errors='coerce')


    data = data.reset_index(drop=True)

    # Remove rows where Category is NaN or all year values are NaN
    data = data[data['Category'].notna() & data.iloc[:, 1:].notna().any(axis=1)]

    return raw, data, years