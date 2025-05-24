import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from tabs.rent_presentations.rent_data import loadRentData, plotRentData

def show_correlation_heatmap(df):
    st.header("📊 Korrelationsanalyse af huslejeindeks 2021 - 2024")
    st.write("Nedenfor ses et heatmap over korrelationerne mellem kvartalerne i 2024.")

    # Sørger for at vi kun kigger på numeriske kolonner (de 4 kvartaler)
    numeric_df = df.select_dtypes(include=["float64", "int64"])

    # Beregner korrelation
    corr = numeric_df.T.corr()

    # Plotter heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.subheader("Forklaring:")
    st.markdown("""
    - En korrelation tæt på **1** betyder, at huslejeudviklingen i de regioner følger hinanden tæt.
    - En korrelation tæt på **0** betyder, at udviklingen er uafhængig.
    - En korrelation tæt på **-1** betyder, at de bevæger sig i modsatte retninger.
    """)

def main():
    st.title("Husleje Heatmap - 2024")

    df = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    if df is not None:
        st.success("Data indlæst korrekt!")
        st.dataframe(df)

        show_correlation_heatmap(df)
    else:
        st.error("Kunne ikke indlæse datafilen.")

if __name__ == "__main__":
    main()
