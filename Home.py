import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="Calorie & Nutrition Tracker", layout="wide")

st.title("🍎 Calorie and Nutrition Tracker")
st.write("Welcome! Track your calorie goals and see your progress over time.")
st.markdown("---")

# --- File setup ---
file_path = "data/meals.csv"
goal_file = "data/goal.txt"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
    pd.DataFrame(columns=["Date", "Meal", "Calories", "Protein", "Carbs", "Fat"]).to_csv(file_path, index=False)

# --- Load CSV ---
df = pd.read_csv(file_path)

expected_cols = ["DateTime", "Date", "MealType", "Meal", "Calories", "Protein", "Carbs", "Fat"]
for col in expected_cols:
    if col not in df.columns:
        df[col] = pd.NaT if col in ["DateTime", "Date"] else None


# --- Handle empty dataset ---
if df.empty:
    st.info("No meals logged yet. Go to 'Food Logging' to add your first meal!")

# --- Goal Calories Section ---
st.header("🎯 Daily Calorie Goal")

if not os.path.exists(goal_file):
    with open(goal_file, "w") as f:
        f.write("2000")  # default goal

with open(goal_file, "r") as f:
    goal_calories = int(f.read().strip())

new_goal = st.number_input("Set or update your daily calorie goal (kcal):", min_value=500, max_value=6000, value=goal_calories, step=50)

if new_goal != goal_calories:
    with open(goal_file, "w") as f:
        f.write(str(new_goal))
    st.success(f"Daily calorie goal updated to {new_goal} kcal!")
    goal_calories = new_goal

# --- Dashboard Section ---
st.header("📊 Your Daily Dashboard")

if not df.empty:
    today = datetime.now().date()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    today_data = df[df["Date"] == today]

    consumed_calories = today_data["Calories"].sum()
    balance = goal_calories - consumed_calories

    col1, col2, col3 = st.columns(3)
    col1.metric("Goal Calories", f"{goal_calories} kcal")
    col2.metric("Consumed", f"{consumed_calories:.0f} kcal")
    col3.metric(
    "Remaining",
    f"{balance:.0f} kcal",
    delta=str(int(-balance) if balance < 0 else int(balance))
)


else:
    st.info("Start logging your meals to see your progress!")

# --- Time Range Selection ---
st.markdown("---")
st.subheader("📆 View Graphs By Time Range")
range_option = st.selectbox("Select Time Range:", ["Day", "Week", "Month", "Year", "Max"], index=0)

# --- Filter Data ---
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

    if range_option == "Day":
        filtered = df[df["Date"] == datetime.now().date()]
    elif range_option == "Week":
        filtered = df[df["Date"] >= (datetime.now().date() - pd.Timedelta(days=7))]
    elif range_option == "Month":
        filtered = df[df["Date"] >= (datetime.now().date() - pd.Timedelta(days=30))]
    elif range_option == "Year":
        filtered = df[df["Date"] >= (datetime.now().date() - pd.Timedelta(days=365))]
    else:
        filtered = df

    # --- Graph 1: Calories Over Time ---
    st.write("### 🔥 Calories Over Time")
    fig, ax = plt.subplots(figsize=(6, 3))  # Smaller graph
    filtered.groupby("Date")["Calories"].sum().plot(ax=ax, marker="o", color="#66B3FF")
    ax.set_ylabel("Calories")
    ax.set_xlabel("Date")
    st.pyplot(fig)

    # --- Graph 2: Nutrient Breakdown ---
    st.write("### 🥗 Nutrient Breakdown")
    fig2, ax2 = plt.subplots(figsize=(4, 4))

    # Handle NaN values safely
    nutrients = filtered[["Protein", "Carbs", "Fat"]].sum().fillna(0)

    # Check if all nutrient values are zero before plotting
    if nutrients.sum() == 0:
        st.info("No nutrient data available to display yet.")
    else:
        nutrients.plot(
            kind="pie",
            autopct="%1.1f%%",
            colors=["#FF9999", "#66B3FF", "#99FF99"],
            ax=ax2
        )
        ax2.set_ylabel("")
        st.pyplot(fig2)


# --- Button to AI Page ---
st.markdown("---")
if st.button("🤖 View AI Suggestions"):
    st.switch_page("pages/2_AI_Suggestions.py")

st.caption("Use the sidebar to navigate to Food Logging or Visualization pages.")
