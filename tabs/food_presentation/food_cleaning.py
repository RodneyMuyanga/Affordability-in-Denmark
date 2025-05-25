import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from scipy.stats.mstats import winsorize
from tabs.food_presentation.food_clean_data import load_and_clean

def show_cleaning():

    df, data, years = load_and_clean()



    st.header("🧹 Data Cleaning Process")

    st.markdown("""
        This section shows how the original data was cleaned and transformed:

        - Rows without product names or with all missing values were removed  
        - All numeric values were converted  
        - Data was reshaped for analysis  
        """)

    st.write(f"Raw data shape: {df.shape}")
    st.write(f"Cleaned data shape: {data.shape}")

           # Vis hvor der er NaN
    nan_counts = data.isna().sum()
    st.write("NaN values in cleaned data (per column):")
    st.write(nan_counts[nan_counts > 0])

    st.write("Column data types (after cleaning):")
    st.write(data.dtypes)

    st.success("✔️ Data has been successfully cleaned. Five rows, for products with no category or only missing values—were dropped, the extra metadata column was removed, and all remaining cells have been converted to numeric.")


       # ── Outlier detection via IQR ──
    st.subheader("🔎 Outlier Detection (IQR Method)")

    # melt to long format
    long = data.melt(
        id_vars="Category",
        value_vars=years,
        var_name="Year",
        value_name="Change"
    )

    def flag_iqr(group):
        q1 = group.Change.quantile(0.25)
        q3 = group.Change.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        group["is_outlier"] = ~group.Change.between(lower, upper)
        return group

    checked = long.groupby("Category").apply(flag_iqr)
    outliers = checked[checked.is_outlier]

    st.write(f"Found {len(outliers)} outlier observations:")
    st.dataframe(outliers.reset_index(drop=True).head(10))

    st.markdown("""
    - **IQR Method:** Marks any value more than 1.5 × IQR below Q1 or above Q3.  
    - Instead of dropping them, we **winsorize**: values below the 5th percentile are set to that boundary,  
    and values above the 95th percentile are capped likewise.
    """)

    # ── Winsorization ──

    winsorized = data.copy()
    for col in years:
        winsorized[col] = winsorize(winsorized[col], limits=(0.05, 0.05))

    demo_cat = "01.1.1.6 Pastaprodukter og couscous" 

    # Hent - og "squeeze" - lige den ene række ud som en Serie
    vals_orig = data.loc[data['Category'] == demo_cat, years].iloc[0].dropna()
    vals_win  = winsorized.loc[winsorized['Category'] == demo_cat, years].iloc[0].dropna()


    # Plot side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(6, 2), constrained_layout=True)
    xmin, xmax = -10, 15

    axes[0].hist(vals_orig.values, bins=10, color='skyblue')
    axes[0].set_title("Original", fontsize=8)
    axes[0].set_xlim(xmin, xmax)

    axes[1].hist(vals_win.values,  bins=10, color='skyblue')
    axes[1].set_title("Winsorized", fontsize=8)
    axes[1].set_xlim(xmin, xmax)

    for ax in axes:
        ax.tick_params(axis='both', labelsize=6)

    st.pyplot(fig, use_container_width=False)


    st.markdown("""
****What changed after winsorization?**
- In the **original** histogram, there’s a single extreme spike on the right that stretches the scale and compresses the rest of the data.  
- After **winsorization**, that extreme value is capped at the 95th percentile, so the right tail pulls in and the distribution looks more balanced.  
- This adjustment highlights the true central spread (approximately –10 % to +8 %) without one outlier skews the axis.
""")



    st.write("### Raw data preview (before cleaning):")
    st.dataframe(df.head(10))

    st.write("### Cleaned data (used for plotting):")
    st.dataframe(data.head(10))
    st.markdown("""
Even though the raw and cleaned tables appear nearly identical, the data has been validated and transformed to ensure accuracy.  
This includes handling missing values, converting numeric values, and aligning columns for plotting.
""")

    st.subheader("🔍 Summary statistics (example category)")

    categories = data['Category'].dropna().unique()
    selected_category = st.selectbox("Choose a category to inspect:", sorted(categories), key="cleaning_dropdown")

    example_row = data[data['Category'] == selected_category].iloc[0, 1:]
    example_values = pd.to_numeric(example_row, errors='coerce')
    st.write(example_values.describe())
    st.markdown("""
The table above summarizes the selected category's annual price changes:

- **count**: Number of available years (non-missing data points)
- **mean**: The average annual change in price  
- **std** (*standard deviation*): How much the price changes vary from year to year  
- **min / max**: The lowest and highest price changes observed  
- **25% / 50% / 75%**: Percentiles that show the spread of data. For example,  
  - 25% of the values are below the **25% percentile**,  
  - 50% (the **median**) splits the data in half,  
  - and 75% of the values are below the **75% percentile**

These statistics help identify whether a category has had stable or volatile price changes over time, and whether prices tend to increase, decrease, or fluctuate.
""")


    st.subheader("📊 Value distribution")
    fig2, ax2 = plt.subplots(figsize=(4, 2), dpi=200, constrained_layout=True)
    ax2.hist(example_values.dropna(), bins=10, color='skyblue')
    ax2.set_title("Distribution of annual price changes", fontsize=8)
    ax2.set_xlabel("Change (%)", fontsize=6)
    ax2.set_ylabel("Frequency", fontsize=6)
    # shrink tick labels on both axes
    ax2.tick_params(axis='x', labelsize=7)
    ax2.tick_params(axis='y', labelsize=7)
    # now hand it off to Streamlit at its native size
    st.pyplot(fig2, use_container_width=False)

    st.markdown("""
The histogram shows that most annual price changes are small,  
but a few years stand out with significantly higher changes — likely due to external events like the 2022–2023 inflation.
""")

    