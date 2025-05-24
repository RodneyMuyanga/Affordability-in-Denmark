import streamlit as st

import streamlit as st

def show_conclusion():
    # Header without emoji to avoid encoding issues
    st.subheader("Conclusion and recommendations")

    # Markdown allows safe use of emojis
    st.markdown("""
    **Key takeaways:**
    - Inflation in 2022–2023 outpaced wage growth, reducing real income.
    - Women and public sector employees were especially affected due to already lower wages.
    - Wages and prices do not always move in sync, making predictions difficult.

    **Business Intelligence as a societal tool:**
    - Monitors wages and inflation in real time and can issue early warnings.
    - Enables identification of vulnerable groups and targeted support.
    - Strengthens the decision-making basis in salary negotiations and economic policy.
    - Increases transparency and makes economic trends easier to understand.

    **The road ahead:**
    - Index student grants and social benefits to inflation.
    - Use real wages—not nominal—in negotiations.
    - Implement BI-based systems to continuously assess purchasing power and inequality.

    **Conclusion:**  
    BI does not solve inflation or inequality – but it provides insight and overview.  
    And that is the first step toward smarter action.
    """)
