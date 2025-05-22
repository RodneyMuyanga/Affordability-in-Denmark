import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

from tabs.food_presentation.food_visualization_foodprices import show_visualization
from tabs.food_presentation.food_visualization_expenditure import show_visualization_expenditure
from tabs.food_presentation.food_presentation import show_presentation
from tabs.food_presentation.food_cleaning import show_cleaning
from tabs.food_presentation.food_conclusions import show_conclusions

def show_food_tab():

    st.header("🥖 Food Data – Presentation")

    agenda = st.radio("📌 Select section", [
        "Purpose and motivation",
        "Data cleaning",
        "Visualization of food prices",
        "Visualization of expenditure",
        "Conclusions"
    ], horizontal=True)

    if agenda == "Purpose and motivation":
        show_presentation()
    elif agenda == "Data cleaning":
        show_cleaning()
    elif agenda == "Visualization of food prices":
        show_visualization()
    elif agenda == "Visualization of expenditure":
        show_visualization_expenditure()
    elif agenda == "Conclusions":
        show_conclusions()

   

