import streamlit as st

# Importer opdaterede præsentationsfiler
from tabs.salary_presentations.salary_presentation import show_presentation
from tabs.salary_presentations.salary_development import show_salary_development
from tabs.salary_presentations.salary_forecast import show_salary_forecast
from tabs.salary_presentations.salary_conclusion import show_conclusion

def show_salary_tab():
    st.header("📊 Salary Data – Presentation")

    agenda = st.radio("📌 Select section", [
        "Purpose and motivation",
        "Salary development over time",
        "Inflation forecast",
        "Conclusion"
    ], horizontal=True)

    if agenda == "Purpose and motivation":
        show_presentation()
    elif agenda == "Salary development over time":
        show_salary_development()
    elif agenda == "Inflation forecast":
        show_salary_forecast()
    elif agenda == "Conclusion":
        show_conclusion()
