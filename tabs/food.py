import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

from tabs.food_presentation.food_visualization import show_visualization
from tabs.food_presentation.food_presentation import show_presentation
from tabs.food_presentation.food_cleaning import show_cleaning

def show_food_tab():

    st.header("🥖 Food Data – Presentation")

    agenda = st.radio("📌 Select section", [
        "Purpose and motivation",
        "Data cleaning",
        "Visualization"
    ], horizontal=True)

    if agenda == "Purpose and motivation":
        show_presentation()
    elif agenda == "Data cleaning":
        show_cleaning()
    elif agenda == "Visualization":
        show_visualization()
   

