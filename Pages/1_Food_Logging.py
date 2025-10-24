import streamlit as st
import pandas as pd
import os

st.title("🍽️ Food Logging")

file_path = "data/meals.csv"

if not os.path.exists(file_path):
    pd.DataFrame(columns=["Meal", "Calories", "Protein", "Carbs", "Fat"]).to_csv(file_path, index=False)

df = pd.read_csv(file_path)

meal = st.text_input("Meal Name")
calories = st.number_input("Calories", min_value=0)
protein = st.number_input("Protein (g)", min_value=0)
carbs = st.number_input("Carbs (g)", min_value=0)
fat = st.number_input("Fat (g)", min_value=0)

if st.button("Add Meal"):
    new_row = {"Meal": meal, "Calories": calories, "Protein": protein, "Carbs": carbs, "Fat": fat}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(file_path, index=False)
    st.success(f"{meal} added successfully!")
