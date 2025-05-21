import streamlit as st
import pandas as pd
import os

def show_salary_tab():
    st.header("📊 Løndata – STANDARDBEREGNET TIMEFORTJENESTE")

    # --- Brugerinput ---
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

    # --- Filsti ---
    base_dir = "Data/Salary"
    if group == "Alle":
        folder = "Stats all 13 - 23 salary"
        prefix = "all"
    elif group == "Mænd":
        folder = "Stats All men 13 - 23 salary"
        prefix = "men"
    else:
        folder = "Stats All women 13 - 23 salary"
        prefix = "women"

    file_path = os.path.join(base_dir, folder, f"{prefix} {year}.xlsx")
    st.caption(f"📂 Indlæser fil: `{file_path}`")

    if not os.path.exists(file_path):
        st.error("❌ Filen findes ikke.")
        return

    try:
        # Indlæs data uden header
        df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")

        # Rens kolonne 2
        df[2] = df[2].astype(str).str.strip()

        # Find række der matcher lønkategori (eksakt match)
        match_row = df[df[2].str.lower() == lønkategori.lower()]
        if match_row.empty:
            st.warning(f"⚠️ '{lønkategori}' ikke fundet i filen.")
            return

        row_idx = match_row.index[0]
        header_row = 2  # sektorer er i række 2 (index 2)
        sektorer = df.loc[header_row, 3:8].tolist()
        værdier = df.loc[row_idx, 3:8].astype(float).round(0)

        # Vis resultat
        df_vis = pd.DataFrame({
            "Sektor": sektorer,
            "Timefortjeneste (kr)": værdier
        })

        st.subheader("📊 Timefortjeneste fordelt på sektor")
        st.dataframe(df_vis, use_container_width=True)
        st.bar_chart(df_vis.set_index("Sektor"))

    except Exception as e:
        st.error(f"❌ Fejl under indlæsning: {e}")
