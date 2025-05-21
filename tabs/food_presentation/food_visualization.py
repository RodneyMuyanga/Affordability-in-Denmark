import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from tabs.food_presentation.food_clean_data import load_and_clean

def show_visualization():

    raw_df, data, years = load_and_clean()
      
    st.header("Visualization")

    st.subheader("📈 Food Price Change (Annual % Change)")

    categories = data['Category'].dropna().unique()
    selected_category = st.selectbox("Choose a food category:", sorted(categories))

    row = data[data['Category'] == selected_category]

    if not row.empty:
        values = row.iloc[0, 1:]
        values.index = pd.Index([str(year)[:-3] for year in years], dtype=str)
        values = pd.to_numeric(values, errors='coerce')

    # --- LINE GRAPH ---
    fig, ax = plt.subplots(figsize=(5, 2.5), dpi=150, constrained_layout=True)
    ax.plot(values.index, values.values, marker='o', linestyle='-', color='royalblue')

    for i, v in enumerate(values):
        if pd.notna(v):
            ax.text(values.index[i], v + 0.5, f"{v:.1f}%", ha='center', fontsize=2)

    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.set_title(f"Annual Price Change: {selected_category}", fontsize=8)
    ax.set_ylabel("Change (%)", fontsize=8)
    ax.set_xlabel("Year (June)", fontsize=8)
    ax.axvline("2022", color='red', linestyle='--', alpha=0.5, linewidth=1.2, label="2022-2023 spike")
    ax.axvline("2023", color='red', linestyle='--', alpha=0.5, linewidth=1.2)
    ax.legend(fontsize=7, loc="upper left")
    # shrink tick labels
    ax.tick_params(axis='x', labelsize=6, rotation=0)  # <-- smaller year labels
    ax.tick_params(axis='y', labelsize=6)             # <-- smaller y-axis labels
    ax.grid(True, linewidth=0.5, alpha=0.7)

    st.pyplot(fig,  use_container_width=False)

    st.markdown("""
    📊 **Insight**:  
    Across many food categories, there is a noticeable price spike in 2022 and 2023.  
    This trend likely reflects post-COVID economic effects, inflation, and increased production costs.
    """)
        

    # Calculate average price change per category
    category_means = (
        data
        .set_index("Category")
        .mean(axis=1, skipna=True)
        .sort_values()
    )

    st.subheader("📊 Average Annual Price Change per Category")

    # make it more compact
    fig3, ax3 = plt.subplots(
        figsize=(4, 8),       # narrower and shorter
        dpi=120,
        constrained_layout=True
    )

    ax3.barh(category_means.index, category_means.values, color='lightgreen')

    # titles & labels
    ax3.set_title(
        "Avg Annual Price Change\nby Category",
        fontsize=10,
        pad=12
    )
    ax3.set_xlabel("Avg Change (%)", fontsize=8)

    # shrink tick labels
    ax3.tick_params(axis='y', labelsize=6)  # category names
    ax3.tick_params(axis='x', labelsize=6)  # numeric axis

    st.pyplot(fig3, use_container_width=False)


    st.markdown("""
        ### 📈 *Insight: Average Annual Price Change by Category*

        The chart above displays the **average annual percentage change in food prices** across categories from 2014 to 2024. Each bar represents how much, on average, the price of a category has changed per year.

        🔍 **Key observations**:
        - **Oils and dairy** categories like *Olivenolie* (olive oil), *Mælk med lavt fedtindhold* (low-fat milk), and *Smør* (butter) show the **highest average increases**, suggesting they have been particularly sensitive to market fluctuations and inflation.  
        - Conversely, items like *Salt*, *Kakaopulver*, and *Færdigretter* (ready meals) exhibit **lower or even negative average changes**, possibly due to stable supply chains or lower demand growth.  
        - The distribution indicates **significant variation** between food types, which is important for understanding **household budget pressure** over time.

        This ranking helps identify which food types have become most expensive over the years and where price pressure is greatest for consumers.
        """)


