import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("🍽️ Food Logging")

file_path = "data/meals.csv"

# Ensure folder and file exist
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
    pd.DataFrame(columns=["DateTime", "Date", "MealType", "Meal", "Calories", "Protein", "Carbs", "Fat"]).to_csv(file_path, index=False)

df = pd.read_csv(file_path)

# --- Meal Input Section ---
st.subheader("Add a New Meal")

meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
meal = st.text_input("Meal Name (e.g., 'Chicken Curry', 'Oatmeal')")
col1, col2, col3, col4 = st.columns(4)
with col1:
    calories = st.number_input("Calories (kcal)", min_value=0)
with col2:
    protein = st.number_input("Protein (g)", min_value=0)
with col3:
    carbs = st.number_input("Carbs (g)", min_value=0)
with col4:
    fat = st.number_input("Fat (g)", min_value=0)

if st.button("➕ Add Meal"):
    if meal.strip() == "":
        st.warning("Please enter a meal name.")
    else:
        new_row = {
            "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Date": datetime.now().date(),
            "MealType": meal_type,
            "Meal": meal.strip(),
            "Calories": calories,
            "Protein": protein,
            "Carbs": carbs,
            "Fat": fat
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_path, index=False)
        st.success(f"{meal_type} - {meal} added successfully!")

# --- Display Logged Meals ---
st.markdown("---")
st.subheader("📋 Logged Meals")

if df.empty:
    st.info("No meals logged yet.")
else:
    st.dataframe(df.tail(10), use_container_width=True)
