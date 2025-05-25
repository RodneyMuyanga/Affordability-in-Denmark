import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from scipy.stats.mstats import winsorize
from tabs.food_presentation.food_clean_data_expenditure import load_and_clean_expenditure

def show_visualization_expenditure():

    df_long, years = load_and_clean_expenditure()

    st.header("🍽️ Household Food Expenditure Over Time")

    tab0, tab1 = st.tabs(["Category Breakdown",
    "Total Expenditure"])

    with tab0:
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

        st.markdown("""
    **Description:**  
    This chart displays the **average annual food expenditure per household** for the selected category between 2014 and 2022.  
    - It highlights how spending on this specific item has evolved over time.  
    - Steady upward trends indicate growing budgetary pressure on households for that category.  
    - Any dips may point to changes in consumption habits or price fluctuations.
    """)

    with tab1:
        st.subheader("Average Total Food Expenditure per Household (DKK)")

        # Filtrer total-forbruget
        total = df_long[df_long["Category"] == "01 FØDEVARER OG IKKE-ALKOHOLISKE DRIKKEVARER"]

        # Plot totalforbrug
        fig_tot, ax_tot = plt.subplots(
            figsize=(4, 1.5),
            dpi=120,
            constrained_layout=True
        )
        ax_tot.plot(
            total["Year"],
            total["Expenditure"],
            marker="o",
            linestyle="-",
            color="darkorange"
        )
        ax_tot.set_title("Total Expenditure (DKK)", fontsize=8, pad=4)
        ax_tot.set_xlabel("Year", fontsize=6)
        ax_tot.set_ylabel("Expenditure (DKK)", fontsize=6)
        ax_tot.tick_params(axis="x", labelsize=5, rotation=0)
        ax_tot.tick_params(axis="y", labelsize=5)
        ax_tot.grid(alpha=0.4, linewidth=0.5)

        st.pyplot(fig_tot, use_container_width=False)
        st.markdown("""
    This chart shows the **average total annual expenditure on food per household** from 2014 to 2022.
    - We observe a **steady increase** year over year, reflecting rising food prices and consumption patterns.
    - The **steepest growth** occurs in 2021–2022, likely driven by inflationary pressures post-COVID.
    """)