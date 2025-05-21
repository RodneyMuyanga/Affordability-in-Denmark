import streamlit as st
import pandas as pd
import os

def show_salary_tab():
    st.header("📊 Løndata – STANDARDBEREGNET TIMEFORTJENESTE")

    # --- DROPDOWNS ---
    group = st.selectbox("Vælg gruppe", ["Alle", "Mænd", "Kvinder"])
    year = st.selectbox("Vælg år", ["2013", "2016", "2020", "2023"])
    lønkategori = st.selectbox(
        "Vælg lønkategori", [
            "STANDARDBEREGNET TIMEFORTJENESTE",
            "Genetillæg pr. standard time",
            "Personalegoder pr. standard time",
            "Uregelmæssige betalinger pr. standard time",
            "Pension inkl. ATP pr. standard time",
            "Basisfortjenesten pr. standard time"
        ]
    )

    # --- FILNAVN ---
    file_dir = "Data/Salary"
    if group == "Alle":
        file_path = os.path.join(file_dir, "Stats all 13 - 23 salary", f"all {year}.xlsx")
    elif group == "Mænd":
        file_path = os.path.join(file_dir, "Stats All men 13 - 23 salary", f"men {year}.xlsx")
    else:
        file_path = os.path.join(file_dir, "Stats All women 13 - 23 salary", f"women {year}.xlsx")

    st.caption(f"📂 Indlæser fil: `{file_path}`")

    try:
        df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")

        # Find række der matcher lønkategori
        match_row = df[df[3].astype(str).str.contains(lønkategori, case=False, na=False)]
        if match_row.empty:
            st.warning(f"⚠️ '{lønkategori}' ikke fundet i filen.")
            return

        # Ekstrahér sektordata (kolonne 4–8)
        værdier = match_row.iloc[0, 4:9].astype(float).round(0)
        sektorer = ["Sektorer i alt", "Stat", "Regioner", "Kommuner", "Virksomheder"]
        df_vis = pd.DataFrame({
            "Sektor": sektorer,
            "Timefortjeneste (kr)": værdier
        })

        # VISNING
        st.subheader("📊 Timefortjeneste fordelt på sektor")
        st.dataframe(df_vis, use_container_width=True)
        st.bar_chart(df_vis.set_index("Sektor"))

    except Exception as e:
        st.error(f"❌ Fejl under indlæsning: {e}")
