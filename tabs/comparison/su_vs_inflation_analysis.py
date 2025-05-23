import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from tabs.SU.su_tab import load_and_clean_data as load_su_data
from tabs.food_presentation.food_clean_data import load_and_clean as load_food_price_data

def prepare_combined_data():
    # Load SU data
    su_df, _, _ = load_su_data(
        file_stipend="Data/SU/SU stipendier og lån (mio. kr.).xlsx",
        file_antal="Data/SU/Antal støttemodtagere og låntagere.xlsx",
        file_aarsvaerk="Data/SU/Støtteårsværk.xlsx",
        file_home="Data/SU/students_living_at_home.xlsx",
        file_not_home="Data/SU/students_not_living_at_home.xlsx"
    )
    
    # Load food price annual changes (percentages)
    _, food_data, years = load_food_price_data()
    
    # Calculate average food price change across all categories per year
    food_avg_changes = food_data.set_index('Category')[years].mean(axis=0).reset_index()
    food_avg_changes.columns = ['Year', 'Food_Price_Inflation']
    
    # Extract only the year part (first 4 chars) from 'Year' strings like '2014M06'
    food_avg_changes['Year_only'] = food_avg_changes['Year'].str[:4]
    
    # Drop original 'Year' column to avoid duplicates
    food_avg_changes = food_avg_changes.drop(columns=['Year'])
    
    # Rename 'Year_only' to 'Year' for merging
    food_avg_changes = food_avg_changes.rename(columns={'Year_only': 'Year'})
    
    # Convert year column to int for filtering
    min_year = int(food_avg_changes['Year'].min())
    max_year = int(food_avg_changes['Year'].max())
    
    # Filter SU data to overlap years with food data
    su_filtered = su_df[(su_df['Aar'] >= min_year) & (su_df['Aar'] <= max_year)].copy()
    su_filtered['Year'] = su_filtered['Aar'].astype(str)
    
    # Calculate year-over-year percentage growth for SU per student
    su_filtered = su_filtered.sort_values('Aar')
    su_filtered['SU_growth_pct'] = su_filtered['SU_pr_student'].pct_change() * 100
    
    # Merge SU data with food inflation on year
    combined = pd.merge(
        su_filtered[['Year', 'SU_pr_student', 'SU_growth_pct']],
        food_avg_changes,
        on='Year',
        how='inner'
    )
    
    # Calculate real SU growth adjusted by food inflation
    combined['Real_SU_growth_pct'] = combined['SU_growth_pct'] - combined['Food_Price_Inflation']
    
    return combined

def plot_comparison(df_combined):
    st.header("📊 Comparison of SU Growth and Food Price Inflation (2014–2024)")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df_combined['Year'], df_combined['SU_pr_student'], color='teal', marker='o', label='SU per Student (DKK)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('SU per Student (DKK)', color='teal')
    ax1.tick_params(axis='y', labelcolor='teal')

    ax2 = ax1.twinx()
    ax2.plot(df_combined['Year'], df_combined['Food_Price_Inflation'], color='orange', marker='s', label='Food Price Inflation (%)')
    ax2.plot(df_combined['Year'], df_combined['SU_growth_pct'], color='purple', marker='^', label='SU Growth (%)')
    ax2.plot(df_combined['Year'], df_combined['Real_SU_growth_pct'], color='green', marker='d', label='Real SU Growth (adj. for inflation)')

    ax2.set_ylabel('Percent Change (%)')
    ax2.tick_params(axis='y')

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    plt.title('SU Amounts vs Food Price Inflation and Growth Rates')
    plt.grid(True)
    plt.tight_layout()

    st.pyplot(fig)

def run_su_vs_inflation_analysis():
    st.title("💰 SU vs Food Price Inflation Comparison")

    combined_df = prepare_combined_data()
    st.dataframe(combined_df)

    # Year selector widget
    years = combined_df['Year'].tolist()
    selected_year = st.selectbox("Select year to analyze:", options=years, index=len(years) - 1)

    # Get data for selected year
    row = combined_df[combined_df['Year'] == selected_year].iloc[0]

    su_growth = row['SU_growth_pct']
    food_inflation = row['Food_Price_Inflation']
    real_su_growth = row['Real_SU_growth_pct']

    # Display summary info
    st.markdown(f"### Year {selected_year} Analysis")
    st.markdown(f"- **SU Growth:** {su_growth:.2f}%")
    st.markdown(f"- **Food Price Inflation:** {food_inflation:.2f}%")
    st.markdown(f"- **Real SU Growth (adj. for inflation):** {real_su_growth:.2f}%")

    if real_su_growth >= 0:
        st.success(f"In {selected_year}, SU kept pace with or exceeded food price inflation.")
    else:
        st.error(f"In {selected_year}, SU growth lagged behind food price inflation.")

    plot_comparison(combined_df)

    st.markdown("""
    ### Insights
    - The teal line shows the absolute SU amount per student increasing over the years.
    - Orange shows average food price inflation annually.
    - Purple is SU growth % year-over-year.
    - Green shows SU growth adjusted by food inflation, indicating if SU increases keep pace with food prices.
    - Values below zero in green mean SU has lagged behind inflation in that year.
    """)

if __name__ == "__main__":
    run_su_vs_inflation_analysis()
