import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from scipy.stats.mstats import winsorize
from tabs.food_presentation.food_clean_data import load_and_clean

def show_visualization():

    raw_df, data, years = load_and_clean()

    st.header("Visualization of food prices")

    tab0, tab1, tab2, tab3, tab4, tab5, = st.tabs(["Overall Trend",
            "Category Trend",
            "Avg Change per Category",
            "Volatility",
            "Cluster Analysis",
            "Compare Three Food Types"
        ])

    with tab2:
        st.subheader("📈 Food Price Change (Annual % Change)")

        categories = data['Category'].dropna().unique()
        selected_category = st.selectbox("Choose a food category:", sorted(categories))

        row = data[data['Category'] == selected_category]

        if not row.empty:
            values = row.iloc[0, 1:]
            values.index = pd.Index(years, dtype=str)
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
        
    with tab1:
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
            figsize=(6, 8),       # narrower and shorter
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
    with tab0:
        # ── 1) Overall Trend ──
        st.subheader("🔄 Overall Trend: Avg Annual Food Price Change")
        yearly_avgs = data[years].mean(axis=0, skipna=True)
        years_labels = pd.Index(years, dtype=str)


        # make this one smaller
        fig0, ax0 = plt.subplots(figsize=(5, 2.5), dpi=150, constrained_layout=True)
        ax0.plot(years_labels, yearly_avgs.values, marker='o', linestyle='-', color='teal')

        ax0.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        ax0.set_title("Avg Annual % Change (all categories)", fontsize=8, pad=6)
        ax0.set_xlabel("Year", fontsize=7)
        ax0.set_ylabel("Avg Change (%)", fontsize=7)

        # shrink tick labels
        ax0.tick_params(axis='x', labelsize=6, rotation=0)
        ax0.tick_params(axis='y', labelsize=6)

        ax0.grid(alpha=0.3, linewidth=0.5)

        st.pyplot(fig0, use_container_width=False)

        st.markdown("""
        This chart shows the **average** annual price change across all food categories:
        - Above 0% = an average price increase  
        - Below 0% = an average price decrease  
        """)

        st.markdown("""We observe that the average food price changes hovered around or below 0 % up until 2021, after which there is a sharp jump in 2022–2023. This suggests a sudden inflationary spike, likely driven by post-COVID disruptions and rising production costs.

    In 2024, the average price change falls back toward 0 %, which may indicate that the market is beginning to stabilize.""")
        
    with tab3:
        # ── Volatility ──
        st.subheader("⚡ Volatility: Std Dev of Annual Price Changes")

        vol = data[years].std(axis=0, skipna=True)
        fig_v, ax_v = plt.subplots(figsize=(4, 2), dpi=120, constrained_layout=True)
        ax_v.plot(years_labels, vol.values, marker='X', linestyle='-', color='seagreen')
        ax_v.set_title("Volatility of Food Price Changes", fontsize=8, pad=6)
        ax_v.set_xlabel("Year", fontsize=7)
        ax_v.set_ylabel("Std Dev (%)", fontsize=7)
        ax_v.tick_params(axis='x', labelsize=6, rotation=0)
        ax_v.tick_params(axis='y', labelsize=6)
        ax_v.grid(alpha=0.3)
        st.pyplot(fig_v, use_container_width=False)

        st.markdown("""
        This chart shows the **yearly standard deviation** of price changes across all food categories:
        - A higher value means that price changes were more dispersed (higher volatility) in that year.  
        - A lower value means that most categories moved together.
        """)
    with tab4:
        # 1) Beregn mean & volatility pr. kategori
        stats = data.set_index("Category")[years].agg(['mean','std'], axis=1)
        stats.columns = ['MeanChange','Volatility']

        # 2) K-Means med 2 klynger
        kmeans = KMeans(n_clusters=2, random_state=0).fit(stats)
        stats['Cluster'] = kmeans.labels_.astype(str)

        # 3) Plot
        fig_c, ax_c = plt.subplots(figsize=(4,3), dpi=120, constrained_layout=True)
        for cluster, grp in stats.groupby('Cluster'):
            ax_c.scatter(grp['MeanChange'], grp['Volatility'], label=f"Cluster {cluster}", s=20)
        ax_c.set_xlabel("Avg Annual Change (%)", fontsize=7)
        ax_c.set_ylabel("Volatility (std dev)", fontsize=7)
        ax_c.set_title("Cluster: Stable vs. Volatile Categories", fontsize=8)
        ax_c.legend(fontsize=6)
        ax_c.grid(alpha=0.3)
        st.pyplot(fig_c, use_container_width=False)

        st.markdown("""
    **Cluster explanation:**  
    - Stable categories (Cluster 0) exhibit low average change & low volatility—prices move smoothly.  
    - Volatile categories (Cluster 1) show either high average change or high dispersion—experiencing large price swings.
    """)

    with tab5:
        # Select three example categories
        keys = [
            "01.1.1.3 Brød",
            "01.1.4.1 Mælk, frisk",
            "01.1.7.1 Grøntsager ekskl. kartofler, frisk"
        ]

        fig_s, ax_s = plt.subplots(
        figsize=(4, 2),        # small width×height
        dpi=150,               # højere densitet
        constrained_layout=True
    )

        for key in keys:
            if key in data['Category'].values:
                row = data[data['Category'] == key].iloc[0, 1:]
                series = pd.to_numeric(row, errors='coerce')
                series.index = [str(y) for y in years]
                ax_s.plot(series.index, series.values, marker='o', markersize=3, label=key)


        ax_s.set_title("Price Development: Bread vs. Milk vs. Vegetables", fontsize=7, pad=4)
        ax_s.set_xlabel("Year", fontsize=6)
        ax_s.set_ylabel("Annual Change (%)", fontsize=6)

        # Krymp tick labels
        ax_s.tick_params(axis='x', labelsize=5, rotation=0)
        ax_s.tick_params(axis='y', labelsize=5)

        ax_s.axhline(0, color='gray', linestyle='--', linewidth=0.6)
        ax_s.legend(fontsize=5, loc="upper left")
        ax_s.grid(alpha=0.3, linewidth=0.4)

        st.pyplot(fig_s, use_container_width=False)


        st.markdown("""
        **Observations:**  
        - Bread and vegetables follow almost the same trend until 2021, but in 2022 bread prices rise more sharply.  
        - Milk are more volatile from year to year, showing large fluctuations both upwards and downwards.
        """)




