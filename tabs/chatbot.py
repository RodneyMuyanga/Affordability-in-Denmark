import streamlit as st
from chatbot_logic import ask_chatbot_about_data  

def show_chatbot_tab():
    st.subheader("🤖 Chatbot – Ask Questions About Economic Data")
    st.markdown("""
    You can ask the chatbot about:
    - 💼 Wage development in Denmark (2013–2023)
    - 🥦 Food prices and consumption
    - 🎓 Student grants (SU) and number of recipients
    - 💹 Inflation and purchasing power

    *E.g., "How have food prices changed?" or "What was the public sector salary in 2020?"*
    """)

    user_question = st.text_input("🔍 What would you like to know?")

    if user_question:
        with st.spinner("Thinking..."):
            response = ask_chatbot_about_data(user_question)
            st.success("Answer:")
            st.write(response)
