import streamlit as st
import matplotlib.pyplot as plt


def plot_living_situation(home_df, not_home_df, year_range):
    st.subheader("Students Living at Home vs Not at Home")
    try:
        combined = home_df.merge(not_home_df, on='Aar', suffixes=('_at_home', '_not_home'))
        combined = combined[(combined['Aar'] >= year_range[0]) & (combined['Aar'] <= year_range[1])]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(combined['Aar'], combined['Count_at_home'], marker='o', label='Living at Home', color='blue')
        ax.plot(combined['Aar'], combined['Count_not_home'], marker='o', label='Not Living at Home', color='green')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Students')
        ax.set_title('Student Living Situation Over Time')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        if st.checkbox("Show living situation data"):
            st.dataframe(combined)

        if st.checkbox("Show growth rates for living situations"):
            start, end = combined.iloc[0], combined.iloc[-1]
            total_years = end['Aar'] - start['Aar']
            for col in ['Count_at_home', 'Count_not_home']:
                start_val = start[col]
                end_val = end[col]
                growth = (end_val - start_val) / start_val
                cagr = (end_val / start_val) ** (1 / total_years) - 1
                st.write(f"📊 {col.replace('_', ' ').title()}:")
                st.write(f" - Total growth: {growth*100:.2f}%")
                st.write(f" - CAGR: {cagr*100:.2f}% per year")
    except Exception as e:
        st.error(f"⚠️ Could not process living situation data: {e}")

