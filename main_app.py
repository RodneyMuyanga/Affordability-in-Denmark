import streamlit as st
from tabs.salary import show_salary_tab
from tabs.su import show_su_tab
from tabs.household import show_household_tab
from tabs.food import show_food_tab

st.title("BI Projekt")

tab1, tab2, tab3, tab4 = st.tabs(["Salary", "SU", "Household", "Food"])

with tab1:
    show_salary_tab()
with tab2:
    show_su_tab()
with tab3:
    show_household_tab()
with tab4:
    show_food_tab()
