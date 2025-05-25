import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tabs.rent_presentations.rent_data import loadRentData
from tabs.SU.data_loading import load_and_clean_data

def compare_rent_vs_su():
    st.title("🏡 Rent Index vs. 🎓 SU per Student")

    df_rent = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    df_su, _, _ = load_and_clean_data(
        "Data/SU/SU stipendier og lån (mio. kr.).xlsx",
        "Data/SU/Antal støttemodtagere og låntagere.xlsx",
        "Data/SU/Støtteårsværk.xlsx",
        "Data/SU/students_living_at_home.xlsx",
        "Data/SU/students_not_living_at_home.xlsx"
    )

    su_data = df_su[["Aar", "SU_pr_student"]].copy()
    su_data = su_data[su_data["Aar"] >= 2021]
    su_data.rename(columns={"Aar": "Year"}, inplace=True)

    rent_avg = df_rent[[f"{y}K4" for y in range(2021, 2025)]].mean(axis=0).reset_index()
    rent_avg.columns = ["Kvartal", "Rent Index"]
    rent_avg["Year"] = rent_avg["Kvartal"].str[:4].astype(int)

    combined = pd.merge(su_data, rent_avg, on="Year", how="inner")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(combined["Year"], combined["SU_pr_student"], marker="o", color="green", label="SU per Student")
    ax1.set_ylabel("SU (DKK)", color="green")
    ax1.tick_params(axis='y', labelcolor="green")

    ax2 = ax1.twinx()
    ax2.plot(combined["Year"], combined["Rent Index"], marker="s", color="purple", label="Rent Index")
    ax2.set_ylabel("Rent Index", color="purple")
    ax2.tick_params(axis='y', labelcolor="purple")

    ax1.set_xlabel("Year")
    ax1.set_title("SU per Student vs. Rent Index")
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    🧾 **Insight:**  
    Her kan man se om SU følger med huslejestigningerne – eller om studerende taber købekraft.
    """)