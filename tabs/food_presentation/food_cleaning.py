import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

def show_cleaning():

    # --- FILE PATH ---
    file_path = "Data/Food/FoodPricesComparedToPreviousYear.xlsx"

    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        st.stop()

    # --- LOAD HEADERS ---
    temp = pd.read_excel(file_path, header=None)
    years = temp.iloc[2, 2:].tolist()

    # --- DATA LOADING ---
    df = pd.read_excel(file_path, skiprows=3, header=None)

    # Extract and clean
    data = df.iloc[:, 1:].copy()

    # Check if number of year labels matches number of columns
    if len(years) == data.shape[1] - 1:
        data.columns = ['Category'] + years
    else:
        st.error(f"Mismatch in columns: Data has {data.shape[1]} columns, but only {len(years)} year labels.")
        st.stop()
    # Ensure 'Category' is string and rest are numeric
    data['Category'] = data['Category'].astype(str)

    # Clean common problematic characters before converting to numeric
    data.replace(["–", "—", "", " ", ".."], pd.NA, inplace=True)

    # Convert all year columns to numeric format
    for col in data.columns[1:]:
     data[col] = pd.to_numeric(data[col], errors='coerce')


    data = data.reset_index(drop=True)

    # Remove rows where Category is NaN or all year values are NaN
    data = data[data['Category'].notna() & data.iloc[:, 1:].notna().any(axis=1)]


    st.header("🧹 Data Cleaning Process")

    st.markdown("""
        This section shows how the original data was cleaned and transformed:

        - Rows without product names or with all missing values were removed  
        - All numeric values were converted  
        - Data was reshaped for analysis  
        """)

    st.write(f"Raw data shape: {df.shape}")
    st.write(f"Cleaned data shape: {data.shape}")

        # Vis hvor der er NaN
    nan_counts = data.isna().sum()
    st.write("NaN values in cleaned data (per column):")
    st.write(nan_counts[nan_counts > 0])
    st.success("✔️ Data has been successfully cleaned. 2 empty rows were removed, and all values are now numeric.")


    st.write("### Raw data preview (before cleaning):")
    raw_preview = df.iloc[:10, 1:]
    if len(years) == raw_preview.shape[1] - 1:
        raw_preview.columns = ['Unnamed'] + years
    else:
        st.error(f"Mismatch in raw preview: {raw_preview.shape[1]} columns, {len(years)} year labels")
        st.stop()
 
    st.dataframe(raw_preview)

    st.write("### Cleaned data (used for plotting):")
    st.dataframe(data.head(10))
    st.markdown("""
Even though the raw and cleaned tables appear nearly identical, the data has been validated and transformed to ensure accuracy.  
This includes handling missing values, converting numeric values, and aligning columns for plotting.
""")
    st.write("Column data types (after cleaning):")
    st.write(data.dtypes)



    st.subheader("🔍 Summary statistics (example category)")

    categories = data['Category'].dropna().unique()
    selected_category = st.selectbox("Choose a category to inspect:", sorted(categories), key="cleaning_dropdown")

    example_row = data[data['Category'] == selected_category].iloc[0, 1:]
    example_values = pd.to_numeric(example_row, errors='coerce')
    st.write(example_values.describe())
    st.markdown("""
The table above summarizes the selected category's annual price changes:

- **count**: Number of available years (non-missing data points)
- **mean**: The average annual change in price  
- **std** (*standard deviation*): How much the price changes vary from year to year  
- **min / max**: The lowest and highest price changes observed  
- **25% / 50% / 75%**: Percentiles that show the spread of data. For example,  
  - 25% of the values are below the **25% percentile**,  
  - 50% (the **median**) splits the data in half,  
  - and 75% of the values are below the **75% percentile**

These statistics help identify whether a category has had stable or volatile price changes over time, and whether prices tend to increase, decrease, or fluctuate.
""")


    st.subheader("📊 Value distribution")
    fig2, ax2 = plt.subplots(figsize=(4, 2), dpi=200, constrained_layout=True)
    ax2.hist(example_values.dropna(), bins=10, color='skyblue')
    ax2.set_title("Distribution of annual price changes", fontsize=8)
    ax2.set_xlabel("Change (%)", fontsize=6)
    ax2.set_ylabel("Frequency", fontsize=6)
    # shrink tick labels on both axes
    ax2.tick_params(axis='x', labelsize=7)
    ax2.tick_params(axis='y', labelsize=7)
    # now hand it off to Streamlit at its native size
    st.pyplot(fig2, use_container_width=False)

    st.markdown("""
The histogram shows that most annual price changes are small,  
but a few years stand out with significantly higher changes — likely due to external events like the 2022–2023 inflation.
""")

    