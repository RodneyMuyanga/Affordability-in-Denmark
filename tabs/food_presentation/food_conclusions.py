import pandas as pd
import streamlit as st

def show_conclusions():

    st.header("🔎 Conclusions & Methodology")
    st.markdown("""
    **Purpose:**  
    We set out to uncover how food prices have evolved in Denmark from 2014 to 2024 and to identify which categories experienced the most instability.
                This analysis set out to understand how annual food-price changes in Denmark influence household food expenditure and to evaluate whether rising prices lead to proportional increases in spending. 
                Our original hypothesis—that higher price inflation would drive up total household food expenditure (in DKK)—held true only up to a point.

- **Key findings:**  
  - From 2014 through 2021, modest price changes coincided with gradually rising food expenditures, suggesting relatively inelastic demand: households absorbed small inflationary pressures by paying more.  
  - In 2022, a sharp price spike (~13 %) still saw total spending climb, but the rate of increase slowed compared to price inflation—indicating the limits of budget flexibility.  
  - In 2022, despite elevated prices, overall food expenditure plateaued or even declined slightly, revealing that once prices exceed certain thresholds, households cut back consumption or substitute away from more expensive items.

- **Implications for BI & decision-making:**  
  - **Threshold effects:** Demand elasticity becomes significant beyond moderate inflation levels. Early warning dashboards should flag rapid price increases in critical categories (e.g., dairy, cereals) to anticipate consumption shifts.  
  - **Category sensitivity:** Dairy and oils exhibited the largest correlation between price spikes and spending cuts. Targeted interventions (e.g., subsidies or alternative supply channels) could soften the impact on vulnerable households.  
  - **Forecasting value:** Combining machine learning (random forest) with time-series smoothing provides a reliable framework to predict spending trends and to simulate “what-if” scenarios under future price shocks.

In sum, while modest food-price inflation can be largely absorbed by Danish households, pronounced spikes force behavior changes—undermining the assumption that spending always scales with price. Business intelligence tools that integrate real-time price monitoring, consumption analytics, and forecast models can empower policymakers and retailers to design timely, data-driven support measures and maintain affordability.
""")
