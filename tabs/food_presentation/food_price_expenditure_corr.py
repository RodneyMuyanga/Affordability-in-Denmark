import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize

from tabs.food_presentation.food_clean_data import load_and_clean          
from tabs.food_presentation.food_clean_data_expenditure import load_and_clean_expenditure 

def show_price_expenditure_correlation():
    _, price_df, price_years = load_and_clean()
    cons_df, exp_years     = load_and_clean_expenditure()

    price_long = price_df.melt(
        id_vars="Category",
        var_name="Year",
        value_name="PriceChange"
    )
    
    price_long["Year"] = price_long["Year"].astype(str).str[:-3]

   
    cons_long = cons_df.copy()
    cons_long["Year"] = cons_long["Year"].astype(str)
  

    merged = price_long.merge(
        cons_long,
        on=["Category","Year"],
        how="inner"
    )

    corrs = (
        merged
        .groupby("Category")
        .apply(lambda g: g["PriceChange"].corr(g["Expenditure"]))
        .dropna()
        .sort_values()
    )
    corr_df = corrs.reset_index().rename(columns={0: "Corr"})

    tab0, tab1, tab2, tab3 = st.tabs(["Price ↔ Expenditure Correlation by Category",
    "Total Expenditure", "Trend Comparison", "Overall Trend"])

    with tab0:
        st.subheader("📊 Price ↔ Expenditure Correlation by Category")
        fig1, ax1 = plt.subplots(
            figsize=(6, max(4, len(corr_df)*0.12)),  
            dpi=120,
            constrained_layout=True
        )
        ax1.barh(corr_df["Category"], corr_df["Corr"], color="skyblue")
        ax1.set_xlabel("Pearson correlation", fontsize=7)
        ax1.set_title("Price change vs. expenditure", fontsize=8)
        ax1.tick_params(axis='x', labelsize=6)
        ax1.tick_params(axis='y', labelsize=6)
        ax1.grid(alpha=0.3, axis="x")
        st.pyplot(fig1, use_container_width=False)

        st.markdown("""
**What this chart shows:**  
The horizontal bars represent the Pearson correlation coefficient between year-over-year price changes and average household expenditure for each food category.  
- **Positive values** (bars to the right of zero) indicate categories where higher price increases tend to go hand-in-hand with higher spending—perhaps reflecting necessity or substitution effects.  
- **Negative values** (bars to the left of zero) mean that steeper price hikes are generally associated with lower consumption spending in those categories.  

By comparing these correlations, we can see which categories’ demand is most sensitive to price fluctuations.
""")


    with tab1:
        st.subheader("🔍 Scatter: PriceChange vs. Expenditure")
        sel = st.selectbox("Pick a category to inspect:", corr_df["Category"].tolist())
        sub = merged[merged["Category"] == sel]

        fig2, ax2 = plt.subplots(
            figsize=(3, 2), 
            dpi=120,
            constrained_layout=True
        )
        ax2.scatter(sub["PriceChange"], sub["Expenditure"], color="orange", s=15)
        ax2.set_xlabel("Price Change (%)", fontsize=7)
        ax2.set_ylabel("Expenditure", fontsize=7)
        ax2.set_title(sel, fontsize=8)
        ax2.tick_params(axis='x', labelsize=6)
        ax2.tick_params(axis='y', labelsize=6)
        ax2.grid(alpha=0.3)
        st.pyplot(fig2, use_container_width=False)

        st.markdown("""
**What this scatterplot shows:**  
Each point represents one year’s data for the selected category:
- **X-axis:** annual percentage price change  
- **Y-axis:** average household expenditure in DKK  

A **rising trend** (upward slope) indicates that when prices went up, households still spent more—perhaps due to necessity or lack of close substitutes.  
A **falling trend** (downward slope) suggests that higher prices led to lower spending, indicating more price-sensitive consumption.
""")
        
    with tab2:
        st.subheader("📈 Trend Comparison: Price vs. Expenditure Over Time")
        sel2 = st.selectbox(
            "Choose a category for trend view:",
            corr_df["Category"].tolist(),
            key="trend_cat"
        )

        # Filtrer de to datasæt for den valgte kategori
        df_price = price_long[price_long["Category"] == sel2]
        df_cons  = cons_long[cons_long["Category"]  == sel2]

        # Find fælles årstal
        common_years = sorted(
            set(df_price["Year"]).intersection(df_cons["Year"]),
            key=lambda y: int(y)
        )

        # Begræns serierne til kun de fælles år
        df_price = df_price[df_price["Year"].isin(common_years)].sort_values("Year")
        df_cons  = df_cons[ df_cons["Year"].isin(common_years) ].sort_values("Year")

        # Opret figur med to y-akser
        fig, ax1 = plt.subplots(
            figsize=(5, 2.5),
            dpi=120,
            constrained_layout=True
        )

        # Plot prisændring på venstre akse
        ax1.plot(
            common_years,
            df_price["PriceChange"].tolist(),
            marker="o",
            linestyle="-",
            color="royalblue",
            label="Price Change (%)"
        )
        ax1.set_xlabel("Year", fontsize=7)
        ax1.set_ylabel("Price Change (%)", fontsize=7)
        ax1.tick_params(axis='x', labelsize=6, rotation=0)
        ax1.tick_params(axis='y', labelsize=6)
        ax1.grid(alpha=0.3)

        # Plot forbrug på højre akse
        ax2 = ax1.twinx()
        ax2.plot(
            common_years,
            df_cons["Expenditure"].tolist(),
            marker="s",
            linestyle="--",
            color="orange",
            label="Expenditure (DKK)"
        )
        ax2.set_ylabel("Expenditure (DKK)", fontsize=7)
        ax2.tick_params(axis='y', labelsize=6)

        # Sammensæt legend fra begge akser
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(
            lines1 + lines2,
            labels1 + labels2,
            fontsize=6,
            loc="upper left"
        )

        st.pyplot(fig, use_container_width=False)

        st.markdown(f"""
**What this comparison shows for *{sel2}*:**  
- The **blue solid line** is the annual percentage *price change*.  
- The **orange dashed line** is the average *household expenditure* in DKK.  
""")
        st.markdown("""
**What this trend comparison shows:**  
Contrary to a “necessity good” pattern, here we see that **higher price increases coincide with lower household spending** in DKK for this category. This suggests:

- **Price sensitivity**: When prices spike, consumers cut back rather than simply paying more.  
- **Substitution effects**: Shoppers may switch to cheaper alternatives or reduce overall consumption of this item.  
- **Budget constraints**: Steep price hikes force households to reprioritize their food budgets, leading to a drop in total expenditure.

In other words, once prices exceed a certain threshold, demand falls off—highlighting the limits of consumers’ willingness or ability to absorb rising costs.
""")
        
    with tab3:
        # ── Overall Trend: Avg Price Change ──
        st.subheader("🔄 Overall Trend: Avg Annual Food Price Change")

        # use price_df & price_years instead of undefined data/years
        yearly_avgs = price_df[price_years].mean(axis=0, skipna=True)
        years_labels = [str(y)[:-3] for y in price_years]

        fig0, ax0 = plt.subplots(figsize=(5, 2.5), dpi=150, constrained_layout=True)
        ax0.plot(years_labels, yearly_avgs.values, marker='o', linestyle='-', color='teal', label="Avg % Change")
        ax0.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        ax0.set_title("Avg Annual % Change (all categories)", fontsize=8, pad=6)
        ax0.set_xlabel("Year", fontsize=7)
        ax0.set_ylabel("Avg Change (%)", fontsize=7)
        ax0.tick_params(axis='x', labelsize=6, rotation=0)
        ax0.tick_params(axis='y', labelsize=6)
        ax0.grid(alpha=0.3, linewidth=0.5)

        # ── Overall Trend: Total Expenditure ──
        # pull "FORBRUG I ALT" from your cons_df & exp_years
        total_ex = cons_df.loc[cons_df["Category"] == "FORBRUG I ALT", exp_years].iloc[0]
        years_cons = exp_years

        ax1 = ax0.twinx()
        ax1.plot([str(y) for y in years_cons],
                 total_ex.values,
                 marker='s',
                 linestyle='--',
                 color='orange',
                 label="Total Expenditure")
        ax1.set_ylabel("Expenditure (DKK)", fontsize=7)
        ax1.tick_params(axis='y', labelsize=6)

        # combine legends
        lines0, labels0 = ax0.get_legend_handles_labels()
        lines1, labels1 = ax1.get_legend_handles_labels()
        ax0.legend(lines0 + lines1, labels0 + labels1, fontsize=6, loc="upper left")

        st.pyplot(fig0, use_container_width=False)

        st.markdown("""
**Average price change vs. total expenditure:**  
- The **teal line** shows the *avg annual % change* in food prices across all categories.  
- The **orange dashed line** shows the *total household expenditure* on food.  

You can see how price inflation and overall spending tracked each other over time:
- From 2014–2021 both lines were relatively stable or gently rising.  
- In 2022–2023, prices jumped sharply and total spending also climbed (though less steeply), reflecting how households adjusted budgets.  
- A slight dip in total expenditure in 2024 suggests that consumers are beginning to pull back as prices stay high.
""")
