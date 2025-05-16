import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from husleje_data import loadRentData, plotRentData
from husleje_heatmap import show_correlation_heatmap

def main():
    st.title("Huslejeanalyse - Danmark 2024")

    df = loadRentData("Huslejeindeks_2024.csv")

    if df is not None:
        st.success("Data indlæst korrekt!")
        st.dataframe(df)

        # Opret to faner
        tab1, tab2 = st.tabs(["Udvikling", "Korrelation"])

        with tab1:
            plotRentData(df)

        with tab2:
            show_correlation_heatmap(df)
    else:
        st.error("Kunne ikke indlæse husleje-datafilen.")

if __name__ == "__main__":
    main()
