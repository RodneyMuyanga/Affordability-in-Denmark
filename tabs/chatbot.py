import streamlit as st
from chatbot_logic import ask_chatbot_about_salary

def show_chatbot_tab():
    st.subheader("🤖 Chatbot – Ask About Salary Data")
    st.markdown("Ask questions based on real salary data from 2013–2023.")

    user_question = st.text_input("What do you want to know about wages or trends?")

    if user_question:
        with st.spinner("Thinking..."):
            response = ask_chatbot_about_salary(user_question)
            st.success("Answer:")
            st.write(response)
