import streamlit as st
from utils.salary_loader import load_salary_data

def show_salary_development():
    st.subheader("📈 Salary by sector and group")

    st.markdown("""
    **🔍 Data Preparation (Sprint 2)**  
    This section demonstrates how salary data has been cleaned, transformed, and visualized to support further BI analysis.

    - Data is extracted from official Excel files for each group and year (ETL pipeline).
    - Only relevant rows and columns are selected and cleaned.
    - Missing and empty values are removed.
    - Sector-based earnings are extracted, reshaped, and visualized.

    > The table below shows average hourly earnings by sector for the selected group and year.
    """)

    group = st.selectbox("Select group", ["All", "Men", "Women"])
    year = st.selectbox("Select year", ["2013", "2016", "2020", "2023"])

    # English display -> Danish file value
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
        
        st.markdown("""
        **✔️ Data Cleaning Summary:**
        - Removed fully empty rows and columns
        - Trimmed category names to avoid mismatches
        - Filtered only the selected wage category
        - Converted earnings to float and rounded values for clarity

        **📊 Visual Representation**
        """)
        
        st.dataframe(df_vis, use_container_width=True)
        st.bar_chart(df_vis.set_index("Sector"))
