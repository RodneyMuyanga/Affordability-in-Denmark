import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tabs.rent_presentations.rent_data import loadRentData
from tabs.food_presentation.food_clean_data import load_and_clean  # brug versionen med inflation

def compare_rent_vs_food():
    st.title("🏡 Rent Index vs. 🛒 Food Inflation")

    df_rent = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    _, df_food, food_years = load_and_clean()

    # Beregn årlig ændring i gennemsnitligt huslejeindeks
    rent_years = [f"{y}K4" for y in range(2021, 2025)]  # Brug 4. kvartal for at matche årsdata
    rent_avg = df_rent[rent_years].mean(axis=0).reset_index()
    rent_avg.columns = ["Year", "Rent Index"]
    rent_avg["Year"] = rent_avg["Year"].str[:4].astype(int)

    food_avg = df_food.set_index("Category")[food_years].mean(axis=0).reset_index()
    food_avg.columns = ["Year", "Food Inflation"]
    food_avg["Year"] = food_avg["Year"].astype(int)

    combined = pd.merge(rent_avg, food_avg, on="Year", how="inner")

    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(combined["Year"], combined["Rent Index"], marker="o", color="teal", label="Rent Index")
    ax1.set_ylabel("Rent Index", color="teal")
    ax1.tick_params(axis='y', labelcolor="teal")

    ax2 = ax1.twinx()
    ax2.plot(combined["Year"], combined["Food Inflation"], marker="s", color="orange", label="Food Inflation")
    ax2.set_ylabel("Food Inflation (%)", color="orange")
    ax2.tick_params(axis='y', labelcolor="orange")

    ax1.set_xlabel("Year")
    ax1.set_title("Rent Index vs. Food Inflation")
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    🔍 **Insight:**  
    Sammenlign udviklingen i husleje og fødevarepriser. Er huslejen steget hurtigere end inflationen på mad?
    """)
