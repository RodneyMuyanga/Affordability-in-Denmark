import streamlit as st

def show_chatbot_tab():
    st.header("🤖 Chatbot Assistant")

    st.markdown("Stil et spørgsmål relateret til løn, inflation, SU, mad eller husholdning og få et intelligent svar.")

    question = st.text_input("💬 Indtast dit spørgsmål:")

    if question:
        # Midlertidigt placeholder-svar
        st.info(f"🤖 (Bot-svar eksempel): 'Tak for dit spørgsmål: \"{question}\" – denne funktion er under udvikling.'")
