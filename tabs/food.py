import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

from tabs.food_presentation.food_visualization_foodprices import show_visualization
from tabs.food_presentation.food_visualization_expenditure import show_visualization_expenditure
from tabs.food_presentation.food_presentation import show_presentation
from tabs.food_presentation.food_cleaning import show_cleaning
from tabs.food_presentation.food_conclusions import show_conclusions
from tabs.food_presentation.food_price_expenditure_corr import show_price_expenditure_correlation
from tabs.food_presentation.food_forecast import show_forecast

def show_food_tab():

    st.header("🥖 Food Data – Presentation")

    agenda = st.radio("📌 Select section", [
        "Purpose",
        "Data cleaning",
        "Food prices",
        "Expenditure",
        "Correlation",
        "Forecast",
        "Conclusions"
    ], horizontal=True)

    if agenda == "Purpose":
        show_presentation()
    elif agenda == "Data cleaning":
        show_cleaning()
    elif agenda == "Food prices":
        show_visualization()
    elif agenda == "Expenditure":
        show_visualization_expenditure()
    elif agenda == "Correlation":
        show_price_expenditure_correlation()
    elif agenda == "Forecast":
        show_forecast()
    elif agenda == "Conclusions":
        show_conclusions()


   

