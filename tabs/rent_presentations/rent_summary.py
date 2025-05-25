import streamlit as st
from tabs.rent_presentations.rent_data import loadRentData

def calc_growth(series):
    start_val = series.iloc[0]
    end_val = series.iloc[-1]
    n_quarters = len(series) - 1
    annualized_growth = ((end_val / start_val) ** (4 / n_quarters) - 1) * 100
    total_growth = ((end_val - start_val) / start_val) * 100
    return total_growth, annualized_growth

def show_summary(df):
    st.header("Huslejeudvikling – Total vækst og årlig vækst")

    for region in df.index:
        series = df.loc[region]
        total, cagr = calc_growth(series)
        st.markdown(f"**{region}**")
        st.write(f"Total vækst: {total:.2f}%")
        st.write(f"Gennemsnitlig årlig vækst (CAGR): {cagr:.2f}%")
        st.markdown("---")



def main():
    df = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    if df is not None:
        show_summary(df)
    else:
        st.error("Kunne ikke indlæse datafilen.")
