import pandas as pd
import os

def load_salary_data(group, year, wage_category):
    base_dir = "Data/Salary"
    if group == "All":
        folder = "Stats all 13 - 23 salary"
        prefix = "all"
    elif group == "Men":
        folder = "Stats All men 13 - 23 salary"
        prefix = "men"
    else:
        folder = "Stats All women 13 - 23 salary"
        prefix = "women"

    file_path = os.path.join(base_dir, folder, f"{prefix} {year}.xlsx")
    if not os.path.exists(file_path):
        return None, f"❌ File not found: {file_path}"

    try:
        df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")

        wage_category_clean = wage_category.lower().strip()

        # Søg lønkategori i hele arket, fleksibelt
        match_row = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(wage_category_clean).any(), axis=1)]
        if match_row.empty:
            all_text = df.apply(lambda row: row.astype(str).str.lower(), axis=1).stack().unique()
            suggestions = [s for s in all_text if wage_category_clean.split()[0] in s][:5]
            return None, f"⚠️ '{wage_category}' not found. Suggestions:\n- " + "\n- ".join(suggestions)

        # Hent første match og forsøg at finde værdier i kolonne 3–7 (ofte der tallene ligger)
        row = match_row.iloc[0]
        values = row[3:8]  # Justér ved behov (kan udvides til [4:9])

        # Forsøg at finde sektorer – enten fra række 2 eller ved fallback
        try:
            sectors = df.loc[2, 3:8].tolist()
            sectors = [s if pd.notna(s) else f"Sektor {i+1}" for i, s in enumerate(sectors)]
        except:
            sectors = [f"Sektor {i+1}" for i in range(5)]

        # Valider og konverter
        values_numeric = pd.to_numeric(values, errors="coerce")
        if values_numeric.isnull().any():
            return None, "❌ Non-numeric or missing values in wage data."

        df_result = pd.DataFrame({
            "Sektor": sectors,
            "Timefortjeneste (kr)": values_numeric.round(0).tolist()
        })

        return df_result, None

    except Exception as e:
        return None, f"❌ Error while reading file: {e}"
