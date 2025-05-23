import pandas as pd
import streamlit as st
import os

def load_and_clean_expenditure():
    
    file_path = "Data/Food/AverageHouseholdConsumption.xlsx"
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        st.stop()

    # --- find årstal i header ---
    temp = pd.read_excel(file_path, header=None)
    years = temp.iloc[2, 2:].tolist()  # 2014, 2015, ...

    # --- indlæs rå data, spring 3 rækker over ---
    raw_df = pd.read_excel(file_path, skiprows=3, header=None)

    # --- vælg B-kolonne (Category) og C-Kolonner (år) ---
    data = raw_df.iloc[:, 1:].copy()

    # --- sæt kolonnenavne ---
    if len(years) == data.shape[1] - 1:
        data.columns = ["Category"] + years
    else:
        st.error(f"Mismatch in columns: data has {data.shape[1]} but years list is {len(years)}")
        st.stop()

    # --- sørg for string + numerisk ---
    data["Category"] = data["Category"].astype(str)
    for yr in years:
        data[yr] = pd.to_numeric(data[yr], errors="coerce")

    # --- drop helt tomme rækker ---
    data = data[data["Category"].notna() & data[years].notna().any(axis=1)]

    # --- melt til long format ---
    df_long = data.melt(
        id_vars="Category",
        value_vars=years,
        var_name="Year",
        value_name="Expenditure"
    )

    # --- convert Year til string (fx "2014") uden slicing ---
    df_long["Year"] = df_long["Year"].astype(int).astype(str)

    return df_long, years