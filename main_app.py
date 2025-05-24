import streamlit as st

# ----- Import tabs -----
from tabs.salary import show_salary_tab
from tabs.SU.su_tab import show_su_tab
from tabs.food import show_food_tab
from tabs.chatbot import show_chatbot_tab
from tabs.rent import show_rent_tab
from tabs.comparison.su_vs_inflation_analysis import run_su_vs_inflation_analysis

# ----- Intro tab -----
def show_intro_tab():
    st.title("📌 Project Introduction")
    st.subheader("The Impact of Inflation on Living Costs in Denmark")

    st.markdown("""
    ### 📌 Why affordability and inflation?

    We are currently experiencing a period of significant inflation in Denmark. This project explores how the rising cost of living has affected everyday expenses – including salaries, student grants, food prices, and housing – over the past 10 years.

    **Focus:**
    - What is inflation, and why does it matter?
    - How do income and key expenses compare over time?
    - How can Business Intelligence provide insights into affordability?

    ### 🎯 BI Problem Definition

    **Context & Challenge**  
    Inflation has reduced the purchasing power of Danish citizens. While wages and SU have increased, so have core expenses like food and rent – and not always at the same pace. This growing imbalance affects affordability and quality of life.

    **Purpose & Research Questions**  
    This project investigates whether incomes in Denmark (2013–2023) have kept up with inflation and how that affects different groups – including students, and gender or sector divisions.

    - Are salaries and SU following the rise in prices?
    - Who is most financially pressured – and why?
    - How do food and housing contribute to economic stress?

    **Expected Solution**  
    Using Business Intelligence tools such as visualizations, statistical methods, and machine learning, we uncover how income and expenses evolve and interact over time.

    **Positive Impact**  
    The results offer insights that can help shape future support schemes, wage negotiations, and public policy – enabling more balanced and equitable economic outcomes.
    """)

    st.markdown("---")
    st.markdown("### 🎯 Project Purpose")
    st.markdown("""
    A Business Intelligence project that investigates how inflation has affected:

    - 📊 **Wage development** (men, women, and sectors)
    - 🎓 **Student grant (SU)** recipients' purchasing power
    - 🛒 **Food prices** and their increase over time

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
    """)

    st.markdown("---")
    st.markdown("### 🧪 Hypotheses")
    st.markdown("""
    - Wages and SU have **not increased at the same rate as inflation and prices**
    - Food has become **relatively more expensive**
    - **Women and public sector workers** are among the most financially pressured groups
    """)

    st.markdown("---")
    st.markdown("### 💡 Solution: Our Streamlit BI Tool")
    st.markdown("""
    - Interactive tabs with data and visualizations:
        - **Wages**: Hourly earnings by gender, sector, and year
        - **SU**: Trends in student support and comparison with living costs
        - **Food**: Price development for selected food items
        - **Chatbot**: Ask questions about inflation and economics

    - The expected solution is a user-friendly, interactive BI application built in Streamlit that visualizes and explains the relationship between real income and inflation.

    - This solution can support better decisions for:
        - 📌 **Policy makers and politicians**
        - 🧾 **Citizens and consumers**
        - 🧑‍🏫 **Students and educators**
        - 🧑‍💼 **Unions and employers**
    """)

    st.markdown("---")
    st.markdown("### 👥 Target Groups")
    st.markdown("""
    - 📌 **Policy makers and politicians**  
    - 🧑‍🏫 **Educators and students**  
    - 🧾 **Citizens and consumers**  
    - 🧑‍💼 **Unions and employers**
    """)

    st.success("➡️ Use the top tabs to explore data on wages, student support, food prices, and inflation analysis.")

# ------------------------------------------------------------------

# ----- Streamlit page setup -----
st.set_page_config(page_title="Inflation & Economy", layout="wide")
st.title("📊 BI Project – How Inflation Affects Society")

# ----- Tabs for navigation -----
tabs = st.tabs([
    "📌 Intro",         # tab0
    "💼 Salary",       # tab1
    "🎓 SU",           # tab2
    "🛒 Food",         # tab3
    "🏡 Rent",         # tab4
    "🤖 Chatbot",      # tab5
    "📊 Comparison"    # tab6
])

with tabs[0]:
    show_intro_tab()
with tabs[1]:
    show_salary_tab()
with tabs[2]:
    show_su_tab()
with tabs[3]:
    show_food_tab()
with tabs[4]:
    show_rent_tab()
with tabs[5]:
    show_chatbot_tab()
with tabs[6]:
    st.header("📊 Comparison Subsections")
    sub_tab = st.radio(
        "Select Comparison View:",
        options=["SU vs Food Inflation"],
        index=0
    )
    if sub_tab == "SU vs Food Inflation":
        run_su_vs_inflation_analysis()
