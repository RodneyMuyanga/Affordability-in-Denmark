import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from tabs.food_presentation.food_clean_data_expenditure import load_and_clean_expenditure

def show_visualization_expenditure():

    df_long, years = load_and_clean_expenditure()

    st.header("🍽️ Household Food Expenditure Over Time")

    # --- dropdown til kategori ---
    sel = st.selectbox(
        "Choose a food category for expenditure:",
        sorted(df_long["Category"].unique()),
        key="expenditure_category"
    )
    subset = df_long[df_long["Category"] == sel]

    # --- plot i lille format ---
    st.subheader(f"Avg Expenditure per Household: {sel}")
    fig, ax = plt.subplots(
        figsize=(4, 1.5),     # mindre figur
        dpi=120,
        constrained_layout=True
    )
    ax.plot(
        subset["Year"],
        subset["Expenditure"],
        marker="s",
        linestyle="-",
        color="orange"
    )

    # --- styling af akser og labels ---
    ax.set_xlabel("Year", fontsize=6)
    ax.set_ylabel("Expenditure (DKK)", fontsize=6)
    ax.tick_params(axis="x", labelsize=5, rotation=0)
    ax.tick_params(axis="y", labelsize=5)
    ax.grid(alpha=0.4, linewidth=0.5)

    st.pyplot(fig, use_container_width=False)