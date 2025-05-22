import pandas as pd
import streamlit as st

def show_presentation():
 
    st.header("📌 Why food prices and household consumption?") 
    st.markdown("""Food is one of the largest items in any family’s budget—and when prices jump, many households must cut back or shift spending. This project explores how annual food-price changes in Denmark over the past decade have affected average household consumption—and what BI insights can tell us about coping strategies going forward.

**Focus:**  
- **What drives food-price fluctuations?** Key factors like global supply shocks, energy costs, and currency changes.  
- **How has household food consumption evolved?** Trends in spending, quantities bought, and shifts between product categories.  
- **Where do price spikes hurt most?** Identifying the categories (e.g., dairy, oils, produce) with the biggest impact on budgets.  
- **How can BI help?** Using data cleaning, visualization, and basic statistical summaries to reveal actionable insights.""")

    st.info("➡️ Use the top menu to navigate through the analysis.")
