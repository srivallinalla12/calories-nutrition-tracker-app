import streamlit as st
import pandas as pd
from datetime import date
from src import database, visualization, recommender

st.set_page_config(page_title="Calorie & Nutrition Tracker", layout="wide")

st.title("🍎 Calorie and Nutrition Tracker")

# Load food log
df = database.load_food_log()

# --- Input Section ---
st.header("Add a Meal")
food_name = st.text_input("Food name")
calories = st.number_input("Calories", min_value=0)
carbs = st.number_input("Carbs (g)", min_value=0)
protein = st.number_input("Protein (g)", min_value=0)
fat = st.number_input("Fat (g)", min_value=0)

if st.button("Add Meal"):
    database.add_food_log(food_name, calories, carbs, protein, fat)
    st.success("Meal added!")

# --- Show Logs ---
st.header("Meal History")
st.dataframe(df)

# --- Visualizations ---
if not df.empty:
    st.header("Visualizations")
    visualization.show_pie_chart(df)
    visualization.show_calorie_trend(df)
    visualization.show_bar_chart(df)

# --- Recommendations ---
st.header("Suggestions")
st.write(recommender.simple_recommendation(df))
