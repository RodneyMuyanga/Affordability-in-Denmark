import streamlit as st
from .data_loading import load_and_clean_data
from .data_quality import show_data_quality_checks
from .plots import plot_line_chart, plot_boxplot, plot_correlation_heatmap, show_conclusions_for_plot_line_chart, show_growth_rates, show_su_growth_summary
from .regression import linear_regression_prediction, train_test_model_analysis
from .living_situation import plot_living_situation
from .conclusions import show_conclusions, show_summary_stats, show_final_conclusion

def show_su_tab():
    st.title("SU per Student Analysis (2000–2024)")

    file_stipend = 'Data/SU/SU stipendier og lån (mio. kr.).xlsx'
    file_antal = 'Data/SU/Antal støttemodtagere og låntagere.xlsx'
    file_aarsvaerk = 'Data/SU/Støtteårsværk.xlsx'
    file_home = 'Data/SU/students_living_at_home.xlsx'
    file_not_home = 'Data/SU/students_not_living_at_home.xlsx'

    df, home_df, not_home_df = load_and_clean_data(file_stipend, file_antal, file_aarsvaerk, file_home, file_not_home)

    year_min, year_max = int(df['Aar'].min()), int(df['Aar'].max())
    year_range = st.slider('Select year range:', year_min, year_max, (year_min, year_max))
    df_filtered = df[(df['Aar'] >= year_range[0]) & (df['Aar'] <= year_range[1])]

    df_filtered = show_data_quality_checks(df_filtered)

    if st.checkbox("Show raw data"):
        st.dataframe(df_filtered)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Line Plot", "Box Plot", "Summary Stats",
        "Regression", "Model Analysis", "Living Situation", "Conclusion"
    ])

    with tab1:
        st.subheader("Average SU per Student Over Time")
        plot_line_chart(df_filtered)
        show_conclusions(df_filtered)
        show_conclusions_for_plot_line_chart(df_filtered)
        show_growth_rates(df)
        show_su_growth_summary(df)
        

    with tab2:
        st.subheader("Boxplot of SU Types")
        plot_boxplot(df_filtered)

    with tab3:
        st.subheader("Summary Statistics")
        show_summary_stats(df_filtered)

    with tab4:
        st.subheader("Linear Regression Prediction")
        linear_regression_prediction(df_filtered)

    with tab5:
        st.subheader("Train/Test Model Analysis & Correlation Heatmap")
        plot_correlation_heatmap(df_filtered)
        train_test_model_analysis(df_filtered)

    with tab6:
        st.subheader("Living Situation of Students")
        plot_living_situation(home_df, not_home_df, year_range)

    with tab7:
        st.subheader("Final Conclusion")
        show_final_conclusion(df_filtered)
