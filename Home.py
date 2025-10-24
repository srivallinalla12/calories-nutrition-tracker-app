import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Page setup
st.set_page_config(page_title="Calorie & Nutrition Tracker", layout="wide")

# App Title
st.title("🍎 Calorie and Nutrition Tracker")

st.write("Welcome! This is your personal dashboard to track calories, meals, and nutrition progress.")
st.markdown("---")

# File path
file_path = "data/meals.csv"

# Ensure data file exists
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(file_path) or os.stat(file_path).st_size == 0 :
    pd.DataFrame(columns=["Meal", "Calories", "Protein", "Carbs", "Fat"]).to_csv(file_path, index=False)

# Read data
df = pd.read_csv(file_path)

# Dashboard Content
st.header("📊 Daily Summary")

if df.empty:
    st.info("No meals logged yet. Go to 'Food Logging' to add your first meal!")
else:
    total_calories = df["Calories"].sum()
    total_protein = df["Protein"].sum()
    total_carbs = df["Carbs"].sum()
    total_fat = df["Fat"].sum()

    # Show summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Calories", f"{total_calories:.0f} kcal")
    col2.metric("Protein", f"{total_protein:.1f} g")
    col3.metric("Carbs", f"{total_carbs:.1f} g")
    col4.metric("Fat", f"{total_fat:.1f} g")

    st.markdown("---")

    # Visualization: Calories per meal
    st.subheader("Calories by Meal")
    fig, ax = plt.subplots()
    df.groupby("Meal")["Calories"].sum().plot(kind="bar", color="#87CEEB", ax=ax)
    ax.set_ylabel("Calories (kcal)")
    ax.set_xlabel("Meal Name")
    st.pyplot(fig)

    # Nutrient breakdown pie chart
    st.subheader("Nutrient Breakdown")
    fig2, ax2 = plt.subplots()
    nutrients = df[["Protein", "Carbs", "Fat"]].sum()
    nutrients.plot(kind="pie", autopct="%1.1f%%", colors=["#FF9999", "#66B3FF", "#99FF99"], ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

st.markdown("---")
st.caption("Use the sidebar to navigate to Food Logging, AI Suggestions, or Visualization pages.")
