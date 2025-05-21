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
        return None, f"File not found: {file_path}"

    try:
        df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")
        df[2] = df[2].astype(str).str.strip()

        match_row = df[df[2].str.lower() == wage_category.lower()]
        if match_row.empty:
            return None, f"'{wage_category}' not found in the file."

        row_idx = match_row.index[0]
        header_row = 2
        sectors = df.loc[header_row, 3:8].tolist()
        values = df.loc[row_idx, 3:8].astype(float).round(0)

        df_result = pd.DataFrame({
            "Sector": sectors,
            "Hourly earnings (DKK)": values
        })

        return df_result, None
    except Exception as e:
        return None, str(e)
