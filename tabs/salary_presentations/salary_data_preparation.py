import streamlit as st
import pandas as pd

def show_salary_data_preparation():
    st.subheader("🧹 Data Preparation for Salary Data")

    st.markdown("""
    This section explains how we processed and cleaned salary data from Statistics Denmark to prepare it for Business Intelligence analysis.

    ---
    
    ### 🧠 Why Data Preparation Matters in BI

    In Business Intelligence, raw data is rarely ready for analysis. Proper preparation ensures:

    - **Accuracy** in comparisons and trends  
    - **Consistency** across years and groups  
    - **Trustworthiness** of BI dashboards  

    ---
    
    ### 🔍 ETL Process (Extract – Transform – Load)

    #### 1️⃣ Extract
    - Data is collected from `.xlsx` files by year (2013–2023) and group (All, Men, Women)
    - Located in subfolders by group
    - Always from the `"LONS30"` sheet

    #### 2️⃣ Transform
    The key data cleaning steps:
    
    - Drop empty rows and columns:
      ```python
      df.dropna(how="all").dropna(axis=1, how="all")
      ```

    - Standardize wage category text and handle missing values:
      ```python
      df[2] = df[2].fillna("ukendt kategori").astype(str).str.strip().str.lower()
      ```

    - Filter by category and extract relevant sectors
    - Validate numeric values and convert:
      ```python
      værdier = pd.to_numeric(værdier, errors='coerce')
      if værdier.isnull().any():
          # Handle non-numeric error
      ```

    - Round to full kr:
      ```python
      værdier.round(0).tolist()
      ```

    #### 3️⃣ Load
    The cleaned data is structured in a simple table:
    ```python
    pd.DataFrame({
        "Sector": [...],
        "Hourly earnings (DKK)": [...]
    })
    ```

    ---
    
    ### ✅ Sprint 2 Requirements

    | Goal           | Fulfilled by |
    |----------------|--------------|
    | **Meaningful** | Extracting relevant wage rows |
    | **Sufficient** | 12 datasets (4 years × 3 groups) |
    | **Shaped**     | Tabular format, clear values |
    | **Cleaned**    | No NaNs, no redundant headers |
    | **Scaled**     | Rounded hourly wage values |
    | **Engineered** | Ready for filtering and charts |

    ---
    """)

    # Vis RAW vs. CLEANED data fra Excel
    st.markdown("### 📊 Example: RAW vs. CLEANED – 2013 & 2023")

    # RAW 2013
    st.markdown("**📄 Raw data – 2013 (first 15 rows):**")
    raw_2013 = pd.read_excel("Data/Salary/Stats all 13 - 23 salary/all 2013.xlsx", sheet_name="LONS30", header=None)
    st.dataframe(raw_2013.head(15), use_container_width=True)

    # CLEANED 2013
    st.markdown("**✅ Cleaned data – 2013 (first 15 rows):**")
    clean_2013 = raw_2013.dropna(how="all").dropna(axis=1, how="all")
    clean_2013[2] = clean_2013[2].fillna("ukendt kategori").astype(str).str.strip().str.lower()
    st.dataframe(clean_2013.head(15), use_container_width=True)

    # RAW 2023
    st.markdown("**📄 Raw data – 2023 (first 15 rows):**")
    raw_2023 = pd.read_excel("Data/Salary/Stats all 13 - 23 salary/all 2023.xlsx", sheet_name="LONS30", header=None)
    st.dataframe(raw_2023.head(15), use_container_width=True)

    # CLEANED 2023
    st.markdown("**✅ Cleaned data – 2023 (first 15 rows):**")
    clean_2023 = raw_2023.dropna(how="all").dropna(axis=1, how="all")
    clean_2023[3] = clean_2023[3].fillna("ukendt kategori").astype(str).str.strip().str.lower()
    st.dataframe(clean_2023.head(15), use_container_width=True)

    # Forskelstabel
    st.markdown("""
    ---
    ### 🔍 Differences Between 2013 and 2023

    | Feature                  | 2013                                 | 2023                                 |
    |--------------------------|---------------------------------------|--------------------------------------|
    | Metadata rows            | Fewer                                 | More (e.g. “Hele landet”)            |
    | Wage categories          | Clean and simple                      | Varying labels and formatting        |
    | Columns                  | Consistent                            | Often shifted or renamed             |
    | Footnotes                | None                                  | Extra rows at the bottom             |

    These changes made it necessary to build **flexible parsing logic** with type checks and missing value handling.
    """)

    st.success("✅ With this process, our salary data is clean, structured, and BI-ready.")
