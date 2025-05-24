import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.salary_loader import load_salary_data

def show_salary_development():
    st.subheader("Salary by sector and group")

    st.markdown("""
    **Data Preparation**  
    This section demonstrates how salary data has been cleaned, transformed, and visualized to support further BI analysis.
    """)

    group = st.selectbox("Select group", ["All", "Men", "Women"])

    folder_map = {
        "All": "Data/Salary/Stats all 13 - 23 salary",
        "Men": "Data/Salary/Stats All men 13 - 23 salary",
        "Women": "Data/Salary/Stats All women 13 - 23 salary"
    }

    selected_folder = folder_map[group]
    file_names = os.listdir(selected_folder)
    available_years = sorted(list({f.split()[1][:4] for f in file_names if f.endswith(".xlsx")}), reverse=False)

    year = st.selectbox("Select year", available_years)

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

    df_vis, error = load_salary_data(group, year, wage_category)

    if error:
        st.error(f"❌ {error}")
    else:
        st.success(f"📂 Data loaded for {group}, {year}")

        explanations = {
            "Sektorer i alt": "Total average across all sectors",
            "Stat": "Government employees including public funds",
            "Stat (inklusive sociale kasser og fonde)": "Government incl. social funds",
            "Regioner": "Employees in regional authorities (e.g. healthcare)",
            "Kommuner": "Municipal employees (e.g. schools, local services)",
            "Virksomheder og organisationer": "Private companies and organizations"
        }

        st.markdown("""
        **Data Cleaning Summary:**
        - Removed fully empty rows and columns
        - Trimmed category names to avoid mismatches
        - Filtered only the selected wage category
        - Converted earnings to float and rounded values for clarity

        **Sector Descriptions:**
        - **Sektor i alt**: Total average across all listed sectors
        - **Stat (inkl. sociale fonde)**: National public sector including social funds
        - **Regioner**: Regional public employees, often healthcare
        - **Kommuner**: Local municipal employees such as teachers, care workers
        - **Virksomheder og organisationer**: Private companies and non-governmental organizations
        
        **Sector-wise Wages – Selected Year**
        """)

        st.dataframe(df_vis, use_container_width=True)
        st.bar_chart(df_vis.set_index("Sektor"))

    # -------------------------
    # Salary development over time
    # -------------------------
    st.markdown("---")
    st.markdown("### Salary development from 2013 to 2023")

    trend_data = []

    for y in available_years:
        df_year, err = load_salary_data(group, y, wage_category)
        if df_year is not None:
            avg_salary = df_year["Timefortjeneste (kr)"].mean()
            trend_data.append({"År": y, "Gennemsnitlig løn (kr)": avg_salary})

    if trend_data:
        df_trend = pd.DataFrame(trend_data).sort_values("År")
        df_trend["År"] = df_trend["År"].astype(str)

        # Beregn procentvis ændring
        df_trend["Procentvis ændring (%)"] = df_trend["Gennemsnitlig løn (kr)"].pct_change() * 100
        df_trend["Procentvis ændring (%)"] = df_trend["Procentvis ændring (%)"].round(2)

        # Line chart – lønniveau
        st.markdown("#### Line Chart – Gennemsnitlig løn over tid")
        st.line_chart(df_trend.set_index("År")[["Gennemsnitlig løn (kr)"]])

        # Bar chart – gennemsnitlig løn
        st.markdown("#### Bar Chart – Gennemsnitlig løn pr. år")
        st.bar_chart(df_trend.set_index("År")[["Gennemsnitlig løn (kr)"]])

        # Punktdiagram – procentvis ændring
        fig, ax = plt.subplots(figsize=(4, 2))
        sns.scatterplot(data=df_trend, x="År", y="Procentvis ændring (%)", s=60, color='blue', ax=ax)
        ax.set_title("Procentvis lønudvikling fra år til år", fontsize=10)
        ax.set_ylabel("Ændring i %", fontsize=9)    
        ax.set_xlabel("År", fontsize=9)
        ax.tick_params(axis='both', labelsize=8)
        ax.grid(True)
        st.pyplot(fig)

        # ✅ Tilføj samlet lønudvikling over hele perioden
        løn_start = df_trend["Gennemsnitlig løn (kr)"].iloc[0]
        løn_slut = df_trend["Gennemsnitlig løn (kr)"].iloc[-1]
        samlet_stigning_pct = ((løn_slut - løn_start) / løn_start) * 100

        st.markdown("#### Samlet lønudvikling over perioden")
        st.metric(
            label=f"Fra {df_trend['År'].iloc[0]} til {df_trend['År'].iloc[-1]}",
            value=f"{samlet_stigning_pct:.2f} %",
            delta=f"{løn_slut - løn_start:.0f} kr."
        )

        # Tabelvisning
        st.markdown("#### 📋 Årlig Procentvis Ændring (tabel)")
        st.dataframe(df_trend[["År", "Procentvis ændring (%)"]], use_container_width=True)

        st.markdown("💬 *Each point shows how much average salary changed compared to the previous year.*")
    else:
        st.warning("⚠️ Could not load trend data across years.")
