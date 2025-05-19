import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

st.sidebar.title("ℹ️ About this app")
st.sidebar.markdown("""
This app visualizes annual price changes of food categories in Denmark.  
The data was cleaned and transformed to ensure meaningful analysis:

- Rows without product names or with all missing values were removed  
- All values were converted to numeric format  
- The data was reshaped into a long format (one row per year per category)

Select a category from the dropdown to view its price change over time.
""")


# --- FILE PATH ---
file_path = "FoodPricesComparedToPreviousYear.xlsx"

# Check if file exists
if not os.path.exists(file_path):
    st.error(f"File not found: {file_path}")
    st.stop()

# --- LOAD FULL FILE TEMPORARILY TO GET YEARS ---
temp = pd.read_excel(file_path, header=None)
years = temp.iloc[2, 2:].tolist()  # row 3 (index 2), from column C (index 2)


# --- DATA LOADING & CLEANING ---
df = pd.read_excel(file_path, skiprows=3, header=None)

# --- EXTRACT HEADERS & DATA ---

# Data = række 4 og nedefter, kolonne B og frem
data = df.iloc[:, 1:].copy()

# Sæt kolonnenavne: først "Category", derefter årstal
data.columns = ['Category'] + years
data = data.reset_index(drop=True)

# Udtræk kolonne 0 (kategori-kolonnen)
categories = df.iloc[:, 1].dropna().unique()

# Extract relevant part (category + values)
data = df.iloc[:, 1:].copy()
data.columns = ['Category'] + years
data = data.reset_index(drop=True)

st.subheader("🧹 Data cleaning process")

st.write("### Raw data preview (before cleaning):")
raw_preview = df.head(10)
raw_preview.columns = ['Unnamed'] + years  # temp naming
st.dataframe(raw_preview)

st.write("### Cleaned and transformed data (used for plotting):")
st.dataframe(data.head(10))

st.subheader("🔍 Summary statistics for selected category")
st.write(values.describe())

st.subheader("📊 Value distribution")
fig2, ax2 = plt.subplots()
ax2.hist(values.dropna(), bins=8, color='skyblue')
ax2.set_title("Distribution of annual price changes")
ax2.set_xlabel("Change (%)")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)


# --- STREAMLIT APP ---
st.title("📈 Food Price Change in Denmark (Annual % Change)")

# Dropdown med kategorier
categories = data['Category'].dropna().unique()
selected_category = st.selectbox("Choose a food category:", sorted(categories))

# Filtrér række
row = data[data['Category'] == selected_category]

if not row.empty:
    values = row.iloc[0, 1:]  # Årsdata
    values.index = pd.Index([str(year)[:-3] for year in years], dtype=str)



    # Konverter til tal
    values = pd.to_numeric(values, errors='coerce')

    # Plot graf
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(values.index, values.values, marker='o', linestyle='-', color='royalblue')

    # Værdier som tekst
    for i, v in enumerate(values):
        if pd.notna(v):
            ax.text(values.index[i], v + 0.5, f"{v:.1f}%", ha='center', fontsize=8)

    ax.axhline(0, color='gray', linestyle='--')  # nul-linje
    ax.set_title(f"Annual Price Change: {selected_category}")
    ax.set_ylabel("Change (%)")
    ax.set_xlabel("Year (June)")
    ax.grid(True)

    st.pyplot(fig)
else:
    st.warning("No data available for the selected category.")