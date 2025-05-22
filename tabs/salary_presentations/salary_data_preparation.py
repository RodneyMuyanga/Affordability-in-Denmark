import streamlit as st

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

    - Standardize wage category text:
      ```python
      df[2] = df[2].astype(str).str.strip().str.lower()
      ```

    - Filter by category and extract relevant sectors
    - Convert values to numeric and round:
      ```python
      df.loc[row_idx, 3:8].astype(float).round(0)
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
    
    ### 📊 Example: RAW vs. CLEANED – 2013

    **Raw excerpt:**
    ```
    Løn efter køn, tid, lønkomponenter og sektor
    Enhed: Kr.
    Mænd og kvinder i alt  2013.0  STANDARDBEREGNET TIMEFORTJENESTE  240.29 ...
    ```

    **Cleaned:**
    ```
    STANDARDBEREGNET TIMEFORTJENESTE  240.29  255.01 ...
    Genetillæg pr. standard time  3.85  2.87 ...
    ```

    ---
    
    ### 📊 Example: RAW vs. CLEANED – 2023

    **Raw excerpt:**
    ```
    Løn efter område, køn, tid, lønkomponenter og sektor
    Enhed: Kr.
    Hele landet  Mænd og kvinder i alt  2023.0  STANDARDBEREGNET TIMEFORTJENESTE  296.75 ...
    ```

    **Cleaned:**
    ```
    STANDARDBEREGNET TIMEFORTJENESTE  296.75  304.15 ...
    Genetillæg pr. standard time  4.51  2.98 ...
    ```

    ---
    
    ### 🔍 Differences Between 2013 and 2023

    | Feature                  | 2013                                 | 2023                                 |
    |--------------------------|---------------------------------------|--------------------------------------|
    | Metadata rows            | Fewer                                 | More (e.g. “Hele landet”)            |
    | Wage categories          | Clean and simple                      | Varying labels and formatting        |
    | Columns                  | Consistent                            | Often shifted or renamed             |
    | Footnotes                | None                                  | Extra rows at the bottom             |

    These changes made it necessary to build **flexible parsing logic**.

    ---
    
    ✅ With this process, our salary data is **clean, structured, and BI-ready**.
    """)

    st.success("Salary data is now prepared and ready for analysis.")
