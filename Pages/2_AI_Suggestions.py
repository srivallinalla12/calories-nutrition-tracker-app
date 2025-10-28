import streamlit as st
import pandas as pd
import os

# Load the dataset
data_path = os.path.join("data", "meals.csv")
meals = pd.read_csv(data_path)

st.title("💡 AI Assistant")

# Ask for user goal using Streamlit selectbox
user_goal = st.selectbox(
    "Select your goal:",
    ["Select...", "Weight Loss", "High Protein", "Balanced Diet"]
)

if user_goal != "Select...":
    st.subheader(f"Your meal plan for today ({user_goal})")

    all_meals = pd.DataFrame()

    if user_goal.lower() == "weight loss":
        for cat in ["Breakfast", "Lunch", "Dinner"]:
            filtered = meals[(meals["Category"] == cat) & (meals["Calories"] <= 400)]
            if not filtered.empty:
                meal_choice = filtered.sample(1)
                all_meals = pd.concat([all_meals, meal_choice[["Meal", "Calories"]]])
            else:
                st.warning(f"No {cat} meals found for this goal.")

    elif user_goal.lower() == "high protein":
        for cat in ["Breakfast", "Lunch", "Dinner"]:
            filtered = meals[(meals["Category"] == cat) & (meals["Protein"] >= 25)]
            if not filtered.empty:
                meal_choice = filtered.sample(1)
                all_meals = pd.concat([all_meals, meal_choice[["Meal", "Calories", "Protein"]]])
            else:
                st.warning(f"No {cat} meals found for this goal.")

    elif user_goal.lower() == "balanced diet":
        for cat in ["Breakfast", "Lunch", "Dinner"]:
            filtered = meals[
                (meals["Category"] == cat)
                & (meals["Calories"].between(350, 500))
                & (meals["Protein"].between(15, 30))
                & (meals["Fat"].between(8, 15))
            ]
            if not filtered.empty:
                meal_choice = filtered.sample(1)
                all_meals = pd.concat([all_meals, meal_choice[["Meal", "Calories", "Protein", "Fat"]]])
            else:
                st.warning(f"No {cat} meals found for this goal.")

    if not all_meals.empty:
        st.dataframe(all_meals.reset_index(drop=True))
    else:
        st.info("No meals match your selected goal. Try another goal.")
