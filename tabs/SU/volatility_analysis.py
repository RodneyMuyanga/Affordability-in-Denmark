import streamlit as st
import matplotlib.pyplot as plt

def show_volatility_analysis(df):
    st.subheader("📉 Volatility Analysis of SU Growth")

    df = df.sort_values('Aar')
    df['SU_growth_pct'] = df['SU_pr_student'].pct_change() * 100
    df['SU_growth_volatility_3yr'] = df['SU_growth_pct'].rolling(window=3).std()

    st.markdown("""
    This shows the 3-year rolling volatility (standard deviation) of SU growth percentage.
    Note: The first two years will not have volatility values because of the 3-year window.
    """)

    # drop NaNs for plotting volatility
    df_vol = df.dropna(subset=['SU_growth_volatility_3yr'])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_vol['Aar'], df_vol['SU_growth_volatility_3yr'], label='3-Year Rolling Volatility')
    ax.set_xlabel("Year")
    ax.set_ylabel("Volatility (% Std Dev)")
    ax.set_title("SU Growth Volatility Over Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    avg_vol = df_vol['SU_growth_volatility_3yr'].mean()
    st.write(f"Average 3-year volatility over period (excluding NaNs): {avg_vol:.2f}%")
