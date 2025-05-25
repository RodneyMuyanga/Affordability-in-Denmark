import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tabs.rent_presentations.rent_data import loadRentData, plotRentData
from tabs.rent_presentations.rent_heatmap import show_correlation_heatmap
from tabs.rent_presentations.rent_boxplot import show_boxplot
from tabs.rent_presentations.rent_growth import show_growth
from tabs.rent_presentations.rent_summary import show_summary
from tabs.rent_presentations.rent_forecast import forecast_rent

from tabs.comparison.rent_vs_suPrStudent import compare_rent_vs_su
from tabs.comparison.rent_vs_food import compare_rent_vs_food

def main():
    st.title("Rent Analysis 2021 – 2024")

    df = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    if df is not None:
        st.dataframe(df)

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Development", 
            "Heatmap – Correlation", 
            "Boxplot", 
            "Growth Rates", 
            "Summary Stats",
            "Forecast",
            "Comparison"
        ])

        with tab1:
            plotRentData(df)

        with tab2:
            show_correlation_heatmap(df)

        with tab3:
            show_boxplot(df)

        with tab4:
            show_growth(df)

        with tab5:
            show_summary(df)

        with tab6:
            forecast_rent(df)

        with tab7:
            compare_rent_vs_su()
            st.markdown("---")
            compare_rent_vs_food()

    else:
        st.error("Could not load the rent data file.")

if __name__ == "__main__":
    main()
