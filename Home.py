import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ------------------------
# PAGE SETUP
# ------------------------
st.set_page_config(page_title="Calorie & Nutrition Tracker", layout="wide")

st.title("🍎 Calorie & Nutrition Tracker")
st.write("Track your food, monitor calories, and stay consistent toward your fitness goals.")
st.markdown("---")

# ------------------------
# FILES & DATA
# ------------------------
MEALS_FILE = "data/meals.csv"
GOAL_FILE = "data/goal.txt"

os.makedirs("data", exist_ok=True)

# Ensure meals file exists
if not os.path.exists(MEALS_FILE) or os.stat(MEALS_FILE).st_size == 0:
    pd.DataFrame(columns=["DateTime","Date","MealType","Meal","Calories","Protein","Carbs","Fat"]).to_csv(MEALS_FILE, index=False)

# Load meals
df = pd.read_csv(MEALS_FILE)

# Convert dates
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

# ------------------------
# LOAD / SAVE DAILY GOAL
# ------------------------
st.header("🎯 Daily Calorie Goal")

# If no goal file exists, create one
if not os.path.exists(GOAL_FILE):
    with open(GOAL_FILE, "w") as f:
        f.write("2000")

# Read goal
with open(GOAL_FILE, "r") as f:
    goal_calories = int(f.read().strip())

# User sets new goal
new_goal = st.number_input("Set your daily calorie goal:", 
                           min_value=500, max_value=6000, 
                           value=goal_calories, step=50)

# Save if changed
if new_goal != goal_calories:
    with open(GOAL_FILE, "w") as f:
        f.write(str(new_goal))
    goal_calories = new_goal
    st.success(f"Updated your daily goal to {goal_calories} kcal ✔")

# ------------------------
# TODAY'S DASHBOARD
# ------------------------
st.header("📊 Today's Overview")

today = datetime.now().date()

if not df.empty:
    today_df = df[df["Date"] == today]

    consumed = today_df["Calories"].sum()
    remaining = max(goal_calories - consumed, 0)

    col1, col2, col3 = st.columns(3)

    col1.metric("Goal", f"{goal_calories} kcal")
    col2.metric("Consumed", f"{consumed:.0f} kcal")
    col3.metric("Remaining", f"{remaining:.0f} kcal")

    # Progress Bar
    progress = min(consumed / goal_calories, 1.0)
    st.progress(progress)

else:
    st.info("Start logging your meals to see your progress.")

# ------------------------
# QUICK LINKS (CARDS)
# ------------------------
def go_to(page_name):
    st.experimental_set_query_params(page=page_name)

st.markdown("---")
st.header("🚀 Quick Navigation")

colA, colB, colC = st.columns(3)

with colA:
    st.markdown("### 🥗 Log Food")
    st.write("Add meals, calories, and nutrition details.")
    if st.button("Go to Food Logging"):
        go_to("1_Food_Logging")

with colB:
    st.markdown("### 📈 Visualizations")
    st.write("View your calories, macros, and trends.")
    if st.button("Go to Visualization"):
        go_to("3_Visualization")

with colC:
    st.markdown("### 🤖 AI Suggestions")
    st.write("Get personalized AI nutrition insights.")
    if st.button("Go to AI Suggestions"):
        go_to("2_AI_Suggestions")
        
st.markdown("---")
st.caption("Use the sidebar to navigate between pages.")
