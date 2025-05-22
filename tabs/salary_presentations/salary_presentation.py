import streamlit as st

def show_presentation():
    st.subheader("📌 Why salary and inflation?")
    
    st.markdown("""
    We are currently experiencing a period of significant inflation.  
    This project examines how **salary development** in Denmark over the past 10 years relates to inflation – and what we can expect going forward.
    
    **Focus**:
    - What is inflation, and why is it a problem?
    - How have wages developed?
    - How can Business Intelligence be used in this context?
    """)
    
    st.info("➡️ Use the top menu to navigate through the analysis.")

    st.divider()
    
    st.subheader("🎯 BI Problem Definition")

    st.markdown("""
    **Context & Challenge**  
    In recent years, inflation has significantly impacted the purchasing power of individuals in Denmark. At the same time, wages have increased, but not necessarily at the same pace. This creates a gap in affordability and living standards that needs to be understood.

    **Purpose & Research Questions**  
    The goal is to investigate whether wage increases in Denmark from 2013 to 2023 have kept up with inflation, and to identify disparities across gender and sector.  
    - Are wage trends aligned with inflation rates?
    - Which sectors or groups are most affected?
    - Can we predict future income challenges?

    **Expected Solution**  
    By applying Business Intelligence methods such as statistical analysis, visualizations, clustering, and machine learning, we aim to uncover patterns and support decision-making based on real data.

    **Positive Impact**  
    The results can help **policymakers**, **economists**, and **citizens** understand wage-inflation dynamics. This can lead to better strategies for income regulation, support schemes, or labor market adjustments.
    """)
