import streamlit as st

def show_presentation():
    st.subheader("📌 Why salary and inflation?")
    
    st.markdown("""
    We are currently experiencing a period of significant inflation.  
    This project examines how **salary development** in Denmark over the past 10 years relates to inflation – and what we can expect going forward.
    
    Focus:
    - What is inflation, and why is it a problem?
    - How have wages developed?
    - How can Business Intelligence be used in this context?
    """)
    
    st.info("➡️ Use the top menu to navigate through the analysis.")
