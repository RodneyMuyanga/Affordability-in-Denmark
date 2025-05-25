import streamlit as st
from .data_loading import load_and_clean_data
from .data_quality import show_data_quality_checks
from .plots import plot_line_chart, plot_boxplot, plot_correlation_heatmap, show_conclusions_for_plot_line_chart, show_growth_rates, show_su_growth_summary
from .regression import linear_regression_prediction, train_test_model_analysis, compare_regression_models
from .living_situation import plot_living_situation
from .conclusions import show_conclusions, show_summary_stats, show_final_conclusion
from .procentile_analysis import show_percentile_analysis
from .volatility_analysis import show_volatility_analysis

def show_su_tab():
    st.title("🎓 SU per Student Analysis (2012–2024)")

    # CSS 
    st.markdown("""
    <style>
        /* Style radio buttons (subtabs) */
        div[role="radiogroup"] > label {
            margin-bottom: 12px;
            font-weight: 600;
            font-size: 16px;
        }
        /* Style main tabs */
        div[data-testid="stTabs"] button[role="tab"] {
            font-weight: 700;
            font-size: 18px;
        }
    </style>
    """, unsafe_allow_html=True)

    file_stipend = 'Data/SU/SU stipendier og lån (mio. kr.).xlsx'
    file_antal = 'Data/SU/Antal støttemodtagere og låntagere.xlsx'
    file_aarsvaerk = 'Data/SU/Støtteårsværk.xlsx'
    file_home = 'Data/SU/students_living_at_home.xlsx'
    file_not_home = 'Data/SU/students_not_living_at_home.xlsx'

    df, home_df, not_home_df = load_and_clean_data(file_stipend, file_antal, file_aarsvaerk, file_home, file_not_home)

    year_min, year_max = int(df['Aar'].min()), int(df['Aar'].max())
    year_range = st.slider('🗕️ Select year range:', year_min, year_max, (year_min, year_max))
    df_filtered = df[(df['Aar'] >= year_range[0]) & (df['Aar'] <= year_range[1])]

    rows_before = len(df_filtered)
    df_filtered = show_data_quality_checks(df_filtered)
    rows_after = len(df_filtered)
    if rows_before != rows_after:
        st.info(f"🔍 {rows_before - rows_after} rows removed due to outlier filtering.")

    with st.expander("🔍 Show raw data"):
        st.dataframe(df_filtered)

    tab_main = st.tabs([
        "📊 Visualization",
        "📈 Stats & Analysis",
        "⚙️ Advanced",
        "🏠 Living Situation",
        "📘 Conclusion"
    ])

    # --- Visualization tab ---
    with tab_main[0]:
        st.markdown("### Choose visualization type:")
        sub_tab = st.radio("", ["📈 Line Plot", "📊 Box Plot"])

        if sub_tab == "📈 Line Plot":
            st.subheader("📈 Average SU per Student Over Time")
            st.markdown("Visualizes the evolution of SU and support types year by year.")
            plot_line_chart(df_filtered)
            show_conclusions(df_filtered)
            show_conclusions_for_plot_line_chart(df_filtered)
            show_growth_rates(df)
            show_su_growth_summary(df)

        elif sub_tab == "📊 Box Plot":
            st.subheader("📊 Boxplot of SU Types")
            st.markdown("Compares the distribution and variation in SU types across years.")
            plot_boxplot(df_filtered)

    # --- Stats & Analysis tab ---
    with tab_main[1]:
        st.markdown("### Select analysis:")
        sub_tab = st.radio("", [
            "📋 Summary Stats",
            "🧼 Regression",
            "🧪 Model Analysis",
            "🎯 Percentile Analysis"
        ])

        if sub_tab == "📋 Summary Stats":
            st.subheader("📋 Summary Statistics")
            st.markdown("View mean, standard deviation, min, and max for key metrics.")
            show_summary_stats(df_filtered)

            with st.expander("💸 Loan Burden per Taker Over Time"):
                st.markdown("""
                **Loan Burden per Taker** = Total loans divided by number of borrowers.  
                Higher values suggest students are taking on more debt.
                """)
                if 'Loan_Burden_per_Taker' in df_filtered.columns and df_filtered['Loan_Burden_per_Taker'].notna().any():
                    st.line_chart(df_filtered.set_index('Aar')['Loan_Burden_per_Taker'])
                else:
                    st.warning("Loan Burden data is missing or not available.")

        elif sub_tab == "🧼 Regression":
            st.subheader("🧼 Linear Regression Prediction")
            st.markdown("Forecasts future SU and support using selected regression models.")
            linear_regression_prediction(df_filtered)

        elif sub_tab == "🧪 Model Analysis":
            st.subheader("🧪 Train/Test Model Analysis & Correlation Heatmap")
            st.markdown("Evaluates model performance and explores feature relationships.")
            plot_correlation_heatmap(df_filtered)
            train_test_model_analysis(df_filtered)
            compare_regression_models(df_filtered)

        elif sub_tab == "🎯 Percentile Analysis":
            st.subheader("🎯 Percentile Analysis of SU per Student")
            st.markdown("Ranks each year based on its SU support level — how generous was it?")
            show_percentile_analysis(df)

    # --- Advanced tab ---
    with tab_main[2]:
        st.markdown("### Advanced analyses:")
        sub_tab = st.radio("", ["📉 Volatility Analysis"])

        if sub_tab == "📉 Volatility Analysis":
            show_volatility_analysis(df_filtered)

    # --- Living Situation tab ---
    with tab_main[3]:
        st.subheader("🏠 Living Situation of Students")
        st.markdown("Compare students living at home vs. away, including yearly growth trends.")
        plot_living_situation(home_df, not_home_df, year_range)

    # --- Conclusion tab ---
    with tab_main[4]:
        st.subheader("📘 Final Conclusion")
        st.markdown("Summarizes trends and growth rates across all support types.")
        show_final_conclusion(df_filtered)
