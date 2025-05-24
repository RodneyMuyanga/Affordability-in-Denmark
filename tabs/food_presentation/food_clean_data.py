import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import re
from scipy.stats.mstats import winsorize

def load_and_clean():

# --- FILE PATH ---
    file_path = "Data/Food/FoodPricesComparedToPreviousYear.xlsx"

    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        st.stop()

    # --- LOAD HEADERS ---
    raw = pd.read_excel(file_path, header=None)
    temp = pd.read_excel(file_path, header=None, nrows=3)
    years = temp.iloc[2, 2:].tolist()

    # ── Step 2: keep only those entries that start with 4 digits
    year_rx = re.compile(r"^(\d{4})")
    price_years = []
    for x in years:
        s = str(x).strip()
        m = year_rx.match(s)
        if m:
            price_years.append(m.group(1))
    if not price_years:
        st.error("No valid year labels found in price header.")
        st.stop()

    # --- DATA LOADING ---
    df = pd.read_excel(file_path, skiprows=3, header=None).iloc[:, 1:].copy()

    df.replace(r"^[\.\s]+$", pd.NA, regex=True, inplace=True)

    # Check if number of year labels matches number of columns
    if len(price_years) == df.shape[1] - 1:
        df.columns = ['Category'] + price_years
    else:
        st.error(f"Mismatch in columns: Data has {df.shape[1]} columns, but only {len(years)} year labels.")
        st.stop()

    # Ensure 'Category' is string and rest are numeric
    df['Category'] = df['Category'].astype(str)

    # Clean common problematic characters before converting to numeric
    df.replace(["–", "—", "", " ", ".."], pd.NA, inplace=True)

    df[price_years] = df[price_years].fillna(0)

    for y in price_years:
        df[y] = pd.to_numeric(df[y], errors="coerce")
    
    df[price_years] = df[price_years].apply(lambda col: winsorize(col, limits=(0.05,0.05)))
    df = df[df["Category"].notna() & df[price_years].notna().any(axis=1)].reset_index(drop=True)

    # Keep only rows whose Category begins with a digit (e.g. "01.1.1.3 …")
    df = df[df["Category"].str.match(r"^\d")]
    df = df.reset_index(drop=True)

    return raw, df, price_years