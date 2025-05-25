import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.salary_loader import load_salary_data
from tabs.food_presentation.food_clean_data import load_and_clean

def run_salary_vs_food_comparison():
    st.title("💼 Salary vs 🛒 Food Prices and Inflation")

    # --- Load food data ---
    _, food_df, price_years = load_and_clean()
    food_avg = food_df.set_index("Category")[price_years].mean(axis=0).reset_index()
    food_avg.columns = ["Year", "Food_Inflation"]
    food_avg["Year"] = food_avg["Year"].astype(int)

    # --- Fixed wage category ---
    wage_category = "standardberegnet timefortjeneste"

    # --- User input: population group ---
    group = st.selectbox("Select population group", ["All", "Men", "Women"])

    # --- Load salary data ---
    salary_data = []
    for year in food_avg["Year"]:
        df, error = load_salary_data(group, str(year), wage_category)
        if df is not None:
            avg_salary = df["Timefortjeneste (kr)"].mean()
            salary_data.append({"Year": year, "Avg Salary": round(avg_salary, 1)})

    salary_df = pd.DataFrame(salary_data)
    if salary_df.empty:
        st.error("No valid salary data found.")
        return

    # --- Merge salary and food ---
    combined = pd.merge(salary_df, food_avg, on="Year", how="inner").sort_values("Year")

    # --- Year selector ---
    available_years = combined["Year"].tolist()
    selected_years = st.multiselect(
        "Select years to include in the analysis:",
        options=available_years,
        default=available_years
    )
    combined = combined[combined["Year"].isin(selected_years)]
    if combined.empty:
        st.warning("No data available for the selected years.")
        return

    # --- Calculate percentage changes ---
    combined["Salary_Growth"] = combined["Avg Salary"].pct_change() * 100
    combined["Real_Salary_Growth"] = combined["Salary_Growth"] - combined["Food_Inflation"]

    # --- Main chart ---
    st.subheader("📈 Average Salary vs. Food Prices")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(combined["Year"], combined["Avg Salary"], marker="o", color="teal", label="Avg Salary (DKK/hour)")
    ax1.set_ylabel("Avg Salary (DKK)", color="teal")
    ax1.tick_params(axis='y', labelcolor="teal")

    ax2 = ax1.twinx()
    ax2.plot(combined["Year"], combined["Food_Inflation"], marker="s", color="orange", label="Food Inflation (%)")
    ax2.set_ylabel("Food Inflation (%)", color="orange")
    ax2.tick_params(axis='y', labelcolor="orange")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    ax1.set_xlabel("Year")
    ax1.set_title("Salary vs. Food Prices and Inflation")
    ax1.grid(True)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    📊 **Explanation:**  
    This chart compares average wages and food price inflation over time.  
    - **Teal line**: Average salary (DKK/hour)  
    - **Orange line**: Average food inflation (%)  
    """)

    # --- Salary growth bar chart ---
    st.markdown("### 📉 Annual Salary Growth (%)")
    fig2, ax2 = plt.subplots()
    ax2.bar(combined["Year"], combined["Salary_Growth"], color="skyblue")
    ax2.axhline(0, color="gray", linestyle="--")
    ax2.set_ylabel("Change (%)")
    ax2.set_title("Year-over-Year Salary Growth")
    st.pyplot(fig2)

    st.markdown("""
    📘 **Insight:**  
    This shows how much wages increased (or decreased) each year.  
    Negative growth indicates loss in purchasing power.  
    """)

    # --- Food inflation line chart ---
    st.markdown("### 🍲 Annual Food Inflation (%)")
    fig3, ax3 = plt.subplots()
    ax3.plot(combined["Year"], combined["Food_Inflation"], marker='o', linestyle='-', color="orange")
    ax3.axhline(0, color="gray", linestyle="--")
    ax3.set_ylabel("Inflation (%)")
    ax3.set_title("Average Annual Change in Food Prices")
    st.pyplot(fig3)

    st.markdown("""
    📙 **Insight:**  
    This shows the average food price change per year.  
    Spikes may reflect economic shocks like COVID, war, or global supply disruptions.  
    """)

    # --- Real wage growth chart ---
    st.markdown("### 💶 Real Salary Growth (adjusted for food inflation)")
    fig4, ax4 = plt.subplots()
    ax4.plot(combined["Year"], combined["Real_Salary_Growth"], marker="d", color="green")
    ax4.axhline(0, color="red", linestyle="--")
    ax4.set_ylabel("Real Change (%)")
    ax4.set_title("Purchasing Power: Salary Growth Minus Food Inflation")
    st.pyplot(fig4)

    st.markdown("""
    🧾 **Insight:**  
    This shows the true change in income after accounting for rising food prices.  
    - Above 0% = real income improves  
    - Below 0% = people can afford less with the same wage  
    """)

    # --- Data table ---
    with st.expander("📄 View comparison data"):
        st.dataframe(combined, use_container_width=True)

    # --- Summary ---
    st.markdown("### 🔍 Summary")
    st.markdown(f"""
    - This analysis shows how average wages and food inflation evolve year by year.  
    - The **real salary growth** metric shows whether workers actually gain or lose purchasing power.  
    - Years like **2022–2023** show clear economic pressure due to high inflation.  
    """)
