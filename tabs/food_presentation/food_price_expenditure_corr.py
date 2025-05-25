import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from tabs.food_presentation.food_clean_data import load_and_clean          
from tabs.food_presentation.food_clean_data_expenditure import load_and_clean_expenditure 

def show_price_expenditure_correlation():
    # 1) Load data
    _, price_df, price_years = load_and_clean()
    cons_df, exp_years       = load_and_clean_expenditure()
    
    # 2) Melt prices → price_long
    price_long = price_df.melt(
        id_vars   = "Category",
        var_name  = "Year",
        value_name= "PriceChange"
    )
    # Trim ’.06’ osv. og hold kun årstallene
    price_long["Year"] = price_long["Year"].astype(int)
    
    # 3) Melt expenditures → exp_long
    #    Brug det OPRINDELIGE brede cons_df her
    exp_long = cons_df.copy()
    exp_long["Year"] = exp_long["Year"].astype(int)
    # så har exp_long allerede præcis de kolonner vi skal bruge

    
    # 4) Merge på Category+Year
    merged = price_long.merge(
        exp_long,
        on=["Category","Year"],
        how="inner"
    )
    
    # 5) Beregn Pearson-korrelation per kategori
    rows = []
    for cat, grp in merged.groupby("Category"):
        corr = grp["PriceChange"].corr(grp["Expenditure"])
        if pd.notna(corr):
            rows.append((cat, corr))
    corr_df = (
        pd.DataFrame(rows, columns=["Category","Corr"])
          .sort_values("Corr", ascending=True)
          .reset_index(drop=True)
    )
    
    # 6) Sæt tabs op
    tab0, tab1, tab2, tab3 = st.tabs([
        "Price ↔ Expenditure Correlation by Category",
        "Scatter",
        "Trend Comparison",
        "Overall Trend"
    ])
    
    # Tab 0: Korrelations-barplot
    with tab0:
        st.subheader("📊 Correlation by Category")
        fig, ax = plt.subplots(
            figsize=(6, max(4, len(corr_df)*0.12)),
            dpi=120, constrained_layout=True
        )
        ax.barh(corr_df["Category"], corr_df["Corr"], color="skyblue")
        ax.set_xlabel("Pearson r")
        ax.set_title("PriceChange vs. Expenditure")
        ax.grid(axis="x", alpha=0.3)

        ax.tick_params(axis='y', labelsize=6)

      
        for label in ax.get_yticklabels():
            label.set_fontsize(6)
     
        st.pyplot(fig, use_container_width=False)

        st.markdown("""
**How to read this chart:**  
- Each horizontal bar shows the **Pearson correlation coefficient (r)** between year-over-year price changes and household expenditure for that food category.  
- **Positive r** (bars to the right of zero) means that when prices rose, spending also tended to rise – suggesting **inelastic demand** or **necessity goods**.  
- **Negative r** (bars to the left of zero) indicates that price increases coincided with drops in spending – a sign of **price sensitivity**.  
- Categories with correlations near **0** show **little or no linear relationship** between price changes and expenditure.  
""")
    
    # Tab 1: Scatter for én kategori
    with tab1:
        
        sel = st.selectbox("Pick a category to inspect:", corr_df["Category"].tolist())
        sub = merged[merged["Category"] == sel]
        st.subheader(f"🔍 {sel}")

        years = sub["Year"].tolist()
        x_pos  = list(range(len(years)))  

        fig, ax = plt.subplots(figsize=(3, 2), dpi=120, constrained_layout=True)

        # Blå scatter: PriceChange over Year
        ax.scatter(
            sub["Year"].astype(str),
            sub["PriceChange"],
            s=20,
            alpha=0.7,
            label="PriceChange (%)",
            color="royalblue",
            marker="o"
        )
        ax.set_xlabel("Year", fontsize=4)
        ax.set_ylabel("PriceChange (%)", color="royalblue", fontsize=6)

        ax.tick_params(axis="y", labelcolor="royalblue", labelsize=6)

        # Orange scatter på sekundær akse: Expenditure over Year
        ax2 = ax.twinx()
        ax2.scatter(
            sub["Year"].astype(str),
            sub["Expenditure"],
            s=20,
            alpha=0.7,
            label="Expenditure (DKK)",
            color="orange",
            marker="s"
        )
        ax2.set_ylabel("Expenditure (DKK)", color="orange", fontsize=6)
        ax2.tick_params(axis="y", labelcolor="orange", labelsize=6)

        ax.tick_params(axis='both', which='major', labelsize=6)
        ax2.tick_params(axis='both', which='major', labelsize=6)

        # Sammensæt legend
        h1, l1 = ax.get_legend_handles_labels() 
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1+h2, l1+l2, loc="upper left", fontsize=6)

        st.pyplot(fig, use_container_width=False)

        st.markdown("""
**Explanation of the scatterplot:**  
- **Blue circles** show the year-over-year **percentage change in food prices** for the selected category, plotted against calendar year.  
- **Orange squares** show the corresponding **average household expenditure** in DKK for that same year and category.  
- If points lie close together in the vertical direction, it means price changes and spending moved in tandem; wide vertical separation indicates a mismatch (e.g., prices up but spending down).  
""")

    
    # Tab 2: Trend comparison for én kategori
    with tab2:
        sel2 = st.selectbox("Trend comparison for…", corr_df["Category"], key="trend2")
        dfp = price_long[price_long["Category"] == sel2].sort_values("Year")
        dfe = exp_long  [exp_long["Category"]   == sel2].sort_values("Year")
        years = sorted(set(dfp["Year"]).intersection(dfe["Year"]), key=int)
        dfp2 = dfp[dfp["Year"].isin(years)]
        dfe2 = dfe[dfe["Year"].isin(years)]

        fig, ax1 = plt.subplots(figsize=(5,2.5), dpi=120, constrained_layout=True)
        ax1.plot(years, dfp2["PriceChange"].tolist(), "-o", label="PriceChange (%)")
        ax1.set_xlabel("Year"); ax1.set_ylabel("PriceChange (%)"); ax1.grid(alpha=0.3)
        ax2 = ax1.twinx()
        ax2.plot(years, dfe2["Expenditure"].tolist(), "--s", color="orange", label="Expenditure")
        ax2.set_ylabel("Expenditure (DKK)")
        h1,l1 = ax1.get_legend_handles_labels(); h2,l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc="upper center", fontsize=6)
        st.pyplot(fig, use_container_width=False)

        st.markdown("""
**Explanation of the scatterplot:**  
- **X-axis** shows the **calendar year** for the selected category.  
- The **blue circles** plot the **year-over-year price change (%)** on the left y-axis.  
- The **orange squares** plot the **average household expenditure (DKK)** on the right y-axis.  

**How to read it:**  
- Years where the blue dots are above zero indicate positive inflation in that category.  
- Corresponding orange squares let you see, for each year, whether higher prices corresponded to higher or lower household spending in DKK each year.
A downward-sloping orange line (e.g. from 2019 to 2020) indicates that spending fell even as prices rose.
If both series climbed together, it would suggest that demand was price-inelastic (consumers continued purchasing despite higher costs)..  
""")

    
    # Tab 3: Overall Trend
    with tab3:
        st.subheader("🔄 Overall Trend: Avg Annual Price & Expenditure")

        mask = "01 FØDEVARER OG IKKE-ALKOHOLISKE DRIKKEVARER"

# 1) Filtrér til kun den ønskede kategori
        total_exp = (
            exp_long[exp_long["Category"] == mask]
            .set_index("Year")["Expenditure"]     # sæt Year som indeks
            .sort_index()                         # sørg for stigende år
)

        # Hvis du bruger samme liste af år som price_long, kan du reindexe:
        years = price_long["Year"].unique().tolist()  # eller din years_labels
        total_exp = total_exp.reindex(years).astype(float)

        # 1) Beregn gennemsnit pr. år
        avg_price = price_long.groupby("Year")["PriceChange"].mean()

        # 2) Kun de år, som begge serier dækker
        common_years = sorted(
            set(avg_price.index).intersection(total_exp.index),
            key=lambda y: int(y)
        )

        # 3) Byg nye serier, sikre samme længde
        price_vals = [avg_price[y] for y in common_years]
        exp_vals   = [total_exp[y]   for y in common_years]

        # 4) Plot med delt x-akse
        fig, ax1 = plt.subplots(figsize=(5, 2.5), dpi=150, constrained_layout=True)
        ax1.plot(common_years, price_vals, "-o", color="teal", label="Avg PriceChange (%)")
        ax1.axhline(0, color="gray", linestyle="--")
        ax1.set_ylabel("Avg PriceChange (%)")
        ax1.set_xlabel("Year")
        ax1.tick_params(axis="x", labelsize=6, rotation=0)

        ax2 = ax1.twinx()
        ax2.plot(common_years, exp_vals, "--s", color="orange", label="Avg Expenditure (DKK)")
        ax2.set_ylabel("Avg Expenditure (DKK)")
        ax2.tick_params(axis="y", labelsize=6)

        # 5) Samlet legend
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=6)

        st.pyplot(fig, use_container_width=False)
