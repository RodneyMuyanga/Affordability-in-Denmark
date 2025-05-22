# data_processing/salary_parser.py

import pandas as pd

def parse_salary_data(file_path: str, lønkategori: str, year: str):
    try:
        df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")

        # Hvis 2023, brug robust matching med .str.contains
        if year == "2023":
            df[3] = df[3].astype(str).str.strip().str.lower()
            lønkategori_clean = lønkategori.lower().strip()

            # Brug str.contains for fleksibel matching
            match_row = df[df[3].str.contains(lønkategori_clean, na=False)]
            if match_row.empty:
                return None, f"⚠️ '{lønkategori}' ikke fundet i 2023-filen."

            # Brug fast liste for sektorer (svarer til kolonner 4–8)
            sektorer = ["Sektorer i alt", "Stat", "Regioner", "Kommuner", "Virksomheder"]
            værdier = match_row.iloc[0, 4:9].astype(float).round(0).tolist()

        else:
            # Standardstruktur for andre år
            df[2] = df[2].astype(str).str.strip().str.lower()
            lønkategori_clean = lønkategori.lower().strip()

            match_row = df[df[2] == lønkategori_clean]
            if match_row.empty:
                return None, f"⚠️ '{lønkategori}' ikke fundet i filen."

            row_idx = match_row.index[0]
            sektorer = df.loc[2, 3:8].tolist()
            værdier = df.loc[row_idx, 3:8].astype(float).round(0).tolist()

        df_vis = pd.DataFrame({
            "Sektor": sektorer,
            "Timefortjeneste (kr)": værdier
        })
        return df_vis, None

    except Exception as e:
        return None, f"❌ Fejl under indlæsning: {e}"
