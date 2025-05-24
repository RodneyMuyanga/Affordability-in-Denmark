def parse_salary_data(file_path: str, lønkategori: str, year: str):
    try:
        df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")

        lønkategori_clean = lønkategori.lower().strip()

        if year == "2023":
            df[3] = df[3].fillna("ukendt kategori").astype(str).str.strip().str.lower()
            match_row = df[df[3].str.contains(lønkategori_clean, na=False)]
            if match_row.empty:
                return None, f"⚠️ '{lønkategori}' ikke fundet i 2023-filen."
            værdier = match_row.iloc[0, 4:9]
            sektorer = ["Sektorer i alt", "Stat", "Regioner", "Kommuner", "Virksomheder"]
        else:
            df[2] = df[2].fillna("ukendt kategori").astype(str).str.strip().str.lower()
            match_row = df[df[2] == lønkategori_clean]
            if match_row.empty:
                return None, f"⚠️ '{lønkategori}' ikke fundet i filen."
            row_idx = match_row.index[0]
            værdier = df.loc[row_idx, 3:8]

            # Forsøg at finde sektorer dynamisk
            sektor_row = df[df.apply(lambda row: row.astype(str).str.contains("sektor", case=False).any(), axis=1)]
            if not sektor_row.empty:
                sektorer = sektor_row.iloc[0, 3:8].tolist()
            else:
                sektorer = ["Sektor 1", "Sektor 2", "Sektor 3", "Sektor 4", "Sektor 5"]

        værdier_numeric = pd.to_numeric(værdier, errors='coerce')
        if værdier_numeric.isnull().any():
            return None, "❌ Ikke-numeriske eller manglende værdier fundet i løndataene."

        værdier_clean = værdier_numeric.round(0).tolist()

        df_vis = pd.DataFrame({
            "Sektor": sektorer,
            "Timefortjeneste (kr)": værdier_clean
        })

        return df_vis, None

    except Exception as e:
        return None, f"❌ Fejl under indlæsning: {e}"
