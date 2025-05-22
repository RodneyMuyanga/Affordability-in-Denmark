import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
from utils.salary_loader import load_salary_data

def show_salary_statistics():
    st.subheader("📊 Statistical Analysis of Salary Data")

    st.markdown("""
    This section presents advanced statistical analysis of salary data using multiple techniques:

    - Descriptive statistics  
    - Z-score outlier detection  
    - Histogram, KDE, boxplot, swarmplot, violinplot  
    - Correlation heatmap (if applicable)
    """)

    group = st.selectbox("Select group", ["All", "Men", "Women"])

    # Dynamisk årliste baseret på filnavne
    folder_map = {
        "All": "Data/Salary/Stats all 13 - 23 salary",
        "Men": "Data/Salary/Stats All men 13 - 23 salary",
        "Women": "Data/Salary/Stats All women 13 - 23 salary"
    }

    selected_folder = folder_map[group]
    file_names = os.listdir(selected_folder)
    available_years = sorted({f.split()[1][:4] for f in file_names if f.endswith(".xlsx")})
    year = st.selectbox("Select year", available_years)

    # Lønkategorier
    wage_mapping = {
        "STANDARD CALCULATED HOURLY EARNINGS": "STANDARDBEREGNET TIMEFORTJENESTE",
        "Bonuses per standard hour": "Genetillæg pr. standard time",
        "Employee benefits per standard hour": "Personalegoder pr. standard time",
        "Irregular payments per standard hour": "Uregelmæssige betalinger pr. standard time",
        "Pension incl. ATP per standard hour": "Pension inkl. ATP pr. standard time",
        "Base earnings per standard hour": "Basisfortjenesten pr. standard time"
    }

    selected_label = st.selectbox("Select wage category", list(wage_mapping.keys()))
    wage_category = wage_mapping[selected_label]

    df, error = load_salary_data(group, year, wage_category)

    if error:
        st.error(f"❌ {error}")
        return

    st.success("✅ Data loaded and cleaned successfully.")

    # ---------------------
    # Descriptive statistics
    # ---------------------
    st.markdown("### 📐 Descriptive Statistics")
    st.dataframe(df.describe().T)

    # ---------------------
    # Outlier detection
    # ---------------------
    st.markdown("### 📏 Outlier Detection using Z-score")
    df["Z-score"] = zscore(df["Timefortjeneste (kr)"])
    st.dataframe(df[["Sektor", "Timefortjeneste (kr)", "Z-score"]])

    outliers = df[df["Z-score"].abs() > 2]
    if not outliers.empty:
        st.warning("⚠️ Potential outliers detected (Z-score > 2 or < -2):")
        st.dataframe(outliers)
    else:
        st.success("No significant outliers detected.")

    # ---------------------
    # Histogram + KDE
    # ---------------------
    st.markdown("### 📊 Histogram with KDE")
    fig1, ax1 = plt.subplots()
    sns.histplot(df["Timefortjeneste (kr)"], kde=True, bins=10, ax=ax1)
    ax1.set_xlabel("Timefortjeneste (kr)")
    st.pyplot(fig1)

    # ---------------------
    # Boxplot
    # ---------------------
    st.markdown("### 📦 Boxplot")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df["Timefortjeneste (kr)"], ax=ax2)
    st.pyplot(fig2)

    # ---------------------
    # Swarmplot
    # ---------------------
    st.markdown("### 🐝 Swarmplot: Sektor vs. Timefortjeneste")
    fig3, ax3 = plt.subplots()
    sns.swarmplot(x="Sektor", y="Timefortjeneste (kr)", data=df, ax=ax3)
    st.pyplot(fig3)

    # ---------------------
    # Violinplot
    # ---------------------
    st.markdown("### 🎻 Violinplot: Sektor vs. Timefortjeneste")
    fig4, ax4 = plt.subplots()
    sns.violinplot(x="Sektor", y="Timefortjeneste (kr)", data=df, ax=ax4)
    st.pyplot(fig4)

    # ---------------------
    # Correlation heatmap
    # ---------------------
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.shape[1] > 1:
        st.markdown("### 🔥 Correlation Heatmap")
        fig5, ax5 = plt.subplots()
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax5)
        st.pyplot(fig5)
    else:
        st.info("Only one numerical column – correlation heatmap skipped.")
