import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tabs.rent_presentations.rent_data import loadRentData

def calculate_growth(df):
    df_growth = df.copy()
    df_growth = df_growth.T
    df_growth = df_growth.pct_change() * 100
    return df_growth.T

def show_growth(df):
    st.header("Vækst i huslejeindeks – Kvartal over kvartal")

    growth_df = calculate_growth(df)

    st.subheader("Vækstkurve per region")
    fig, ax = plt.subplots(figsize=(12, 6))
    growth_df.T.plot(ax=ax, marker='o')
    ax.set_title("Kvartal-vækst i huslejeindeks")
    ax.set_xlabel("Kvartal")
    ax.set_ylabel("Vækst (%)")
    ax.axhline(0, color='gray', linestyle='--')
    ax.legend(title="Region")
    st.pyplot(fig)

    if st.checkbox("Vis vækstrate tabel"):
        st.dataframe(growth_df.round(2))

def main():
    df = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    if df is not None:
        show_growth(df)
    else:
        st.error("Kunne ikke indlæse datafilen")
