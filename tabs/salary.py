import streamlit as st

# Importer opdaterede præsentationsfiler
from tabs.salary_presentations.salary_presentation import show_presentation
from tabs.salary_presentations.salary_development import show_salary_development
from tabs.salary_presentations.salary_forecast import show_salary_forecast
from tabs.salary_presentations.salary_conclusion import show_conclusion
from tabs.salary_presentations.salary_data_preparation import show_salary_data_preparation
from tabs.salary_presentations.salary_statistics import show_salary_statistics
from tabs.salary_presentations.salary_agenda import show_salary_agenda


def show_salary_tab():
    st.header("📊 Salary Data – Presentation")

    agenda = st.radio("📌 Select section", [
        "Agenda",
        "Purpose and motivation",
        "Data preparation",
        "Salary development over time",
        "Statistical Analysis",
        "Inflation forecast",
        "Conclusion"
    ], horizontal=True)

    if agenda == "Agenda":
        show_salary_agenda()
    elif agenda == "Purpose and motivation":
        show_presentation()
    elif agenda == "Data preparation":
        show_salary_data_preparation()
    elif agenda == "Salary development over time":
        show_salary_development()
    elif agenda == "Statistical Analysis":
        show_salary_statistics()
    elif agenda == "Inflation forecast":
        show_salary_forecast()
    elif agenda == "Conclusion":
        show_conclusion()

    
