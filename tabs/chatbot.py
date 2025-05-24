import streamlit as st
from chatbot_logic import ask_chatbot_about_data  # korrekt funktion

def show_chatbot_tab():
    st.subheader("🤖 Chatbot – Stil spørgsmål om økonomiske data")
    st.markdown("""
    Du kan spørge chatbotten om:
    - 💼 Lønudvikling i Danmark (2013–2023)
    - 🥦 Fødevarepriser og forbrug
    - 🎓 SU og antal modtagere
    - 💹 Inflation og købekraft

    *Fx: "Hvordan har fødevarepriserne ændret sig?" eller "Hvad var lønnen i staten i 2020?"*
    """)

    user_question = st.text_input("🔍 Hvad vil du gerne vide?")

    if user_question:
        with st.spinner("Tænker..."):
            response = ask_chatbot_about_data(user_question)
            st.success("Svar:")
            st.write(response)
