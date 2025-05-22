import streamlit as st
from tabs.salary import show_salary_tab
from tabs.su import show_su_tab
from tabs.household import show_household_tab
from tabs.food import show_food_tab
from tabs.chatbot import show_chatbot_tab

# -------- Intro tab with project overview --------
def show_intro_tab():
    st.title("📌 Project Introduction")
    st.subheader("The Impact of Inflation on Wages, Student Grants, Food, and Household Costs")

    st.markdown("---")
    st.markdown("### 🎯 Project Purpose")
    st.markdown("""
    A Business Intelligence project that investigates how inflation has affected:

    - 📊 **Wage development** (men, women, and sectors)
    - 🎓 **Student grant (SU)** recipients' purchasing power
    - 🛒 **Food prices** and their increase over time
    - 🏠 **Household expenses** and how they've changed

    The project focuses on the period **2013–2023**, during which inflation has impacted the financial wellbeing of many Danes.
    """)

    st.markdown("---")
    st.markdown("### ❓ Problem Statement")
    st.markdown("""
    - Have wages and SU kept up with inflation and price increases?
    - Which groups are losing real purchasing power?
    - Are there imbalances between gender, sectors, or population groups?
    """)

    st.markdown("---")
    st.markdown("### 🔍 Research Questions")
    st.markdown("""
    - How has **real wage** developed in Denmark?
    - Have **students** lost purchasing power over time?
    - Which food items have increased most in price?
    - How is the average **household** economically affected?
    """)

    st.markdown("---")
    st.markdown("### 🧪 Hypotheses")
    st.markdown("""
    - Wages and SU have **not increased at the same rate as inflation and prices**
    - Food and household expenses have become **relatively more expensive**
    - **Women and public sector workers** are among the most financially pressured groups
    """)

    st.markdown("---")
    st.markdown("### 💡 Solution: Our Streamlit BI Tool")
    st.markdown("""
    - Interactive tabs with data and visualizations:
        - **Wages**: Hourly earnings by gender, sector, and year
        - **SU**: Trends in student support and comparison with living costs
        - **Food**: Price development for selected food items
        - **Households**: Estimated budget and expense levels over time
        - **Chatbot**: Ask questions about inflation and economics

    - The expected solution is a user-friendly, interactive BI application built in Streamlit that visualizes and explains the relationship between real income and inflation.

    - It enables exploration of socio-economic trends, comparisons, and deeper understanding of living costs.

    - This solution can support better decisions for:
        - 📌 **Policy makers and politicians** (e.g. for reforms or new initiatives)
        - 🧾 **Citizens and consumers** (who want insight and awareness)
        - 🧑‍🏫 **Students and educators** (for analysis and learning)
        - 🧑‍💼 **Unions and employers** (for negotiations and real wage evaluation)
    """)

    st.markdown("---")
    st.markdown("### 👥 Target Groups")
    st.markdown("""
    - 📌 **Policy makers and politicians**  
    - 🧑‍🏫 **Educators and students**  
    - 🧾 **Citizens and consumers**  
    - 🧑‍💼 **Unions and employers**
    """)

    st.success("➡️ Use the top tabs to explore data on wages, student support, food prices, and household expenses.")
# ------------------------------------------------------------------

# --------- App Layout with tabs ---------
st.set_page_config(page_title="Inflation & Economy", layout="wide")
st.title("📊 BI Project – How Inflation Affects Society")

tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["📌 Intro", "💼 Salary", "🎓 SU", "🛒 Food", "🏠 Household", "🤖 Chatbot"])

with tab0:
    show_intro_tab()
with tab1:
    show_salary_tab()
with tab2:
    show_su_tab()
with tab3:
    show_food_tab()
with tab4:
    show_household_tab()
with tab5:
    show_chatbot_tab()
