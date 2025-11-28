import streamlit as st
import pandas as pd
import os
from datetime import datetime

def home_page():
    st.set_page_config(page_title="Calorie & Nutrition Tracker", layout="wide")
    
    username = st.session_state.get("user", "demo")   # logged-in user

    st.title("🍎 Calorie & Nutrition Tracker")
    st.write("Track your food, monitor calories, and stay consistent toward your fitness goals.")
    st.markdown("---")

    # -------------------------------------------------
    # USER-SPECIFIC OR DEMO FILE PATHS
    # -------------------------------------------------
    os.makedirs("data", exist_ok=True)

    if username == "demo":
        MEALS_FILE = "data/meals.csv"
        GOAL_FILE = "data/goal.txt"
    else:
        MEALS_FILE = f"data/{username}_meals.csv"
        GOAL_FILE = f"data/goal_{username}.txt"

    # -------------------------------------------------
    # MEALS CSV INITIALIZATION
    # -------------------------------------------------
    if not os.path.exists(MEALS_FILE) or os.stat(MEALS_FILE).st_size == 0:
        empty_df = pd.DataFrame(columns=[
            "DateTime", "Date", "MealType", "Meal",
            "Calories", "Protein", "Carbs", "Fat"
        ])
        empty_df.to_csv(MEALS_FILE, index=False)

    df = pd.read_csv(MEALS_FILE)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

    # -------------------------------------------------
    # CALORIE GOAL HANDLING
    # -------------------------------------------------
    st.header("🎯 Daily Calorie Goal")

    if not os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, "w") as f:
            f.write("2000")

    with open(GOAL_FILE, "r") as f:
        goal_calories = int(f.read().strip())

    new_goal = st.number_input(
        "Set your daily calorie goal:",
        min_value=500, max_value=6000,
        value=goal_calories, step=50
    )

    if new_goal != goal_calories:
        with open(GOAL_FILE, "w") as f:
            f.write(str(new_goal))
        goal_calories = new_goal
        st.success(f"Updated your daily goal to {goal_calories} kcal ✔")

    # -------------------------------------------------
    # TODAY'S DASHBOARD
    # -------------------------------------------------
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

        progress = min(consumed / goal_calories, 1.0)
        st.progress(progress)
    else:
        st.info("Start logging your meals to see your progress.")

    # -------------------------------------------------
    # QUICK NAVIGATION
    # -------------------------------------------------
    st.markdown("---")
    st.header("🚀 Quick Navigation")
    st.write("Double Click On The Buttons Below To go To That Page")

    def go_to(page_name):
        st.session_state["page"] = page_name

    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown("### 🥗 Log Food")
        st.write("Add meals, calories, and nutrition details.")
        if st.button("Go to Food Logging"):
            go_to("Food Logging")

    with colB:
        st.markdown("### 📈 Visualizations")
        st.write("View your calories, macros, and trends.")
        if st.button("Go to Visualization"):
            go_to("Visualization")

    with colC:
        st.markdown("### 🤖 AI Suggestions")
        st.write("Get personalized AI nutrition insights.")
        if st.button("Go to AI Suggestions"):
            go_to("AI Suggestions")

    st.markdown("---")
    st.caption("Use the sidebar to navigate between pages.")
