import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from tabs.rent_presentations.rent_data import loadRentData

def show_boxplot(df):
    st.header("Boxplot – Huslejeindeks per kvartal (2021–2024)")

    df_t = df.T  # kvartaler som index
    df_melted = df_t.reset_index().melt(id_vars="index", var_name="Region", value_name="Indeks")
    df_melted.rename(columns={"index": "Kvartal"}, inplace=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="Kvartal", y="Indeks", data=df_melted, palette="pastel")
    plt.xticks(rotation=45)
    
    ax.set_title("Fordeling af huslejeindeks per kvartal")
    st.pyplot(fig)



def main():
    df = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    if df is not None:
        show_boxplot(df)
    else:
        st.error("Kunne ikke indlæse datafilen.")
