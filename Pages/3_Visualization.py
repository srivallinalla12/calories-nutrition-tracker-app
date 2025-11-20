# 3_Visualization.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

st.title("📊 Nutrition Visualization (Protein, Carbs, Fat Focus)")

# ---------------------------
# Load Meals
# ---------------------------
MEALS_FILE = "data/meals.csv"
try:
    df = pd.read_csv(MEALS_FILE)
except FileNotFoundError:
    st.warning("No saved daily logs found yet. Log meals on the Food Logging page first.")
    st.stop()

# Ensure datetime columns
df["DateTime"] = pd.to_datetime(df["DateTime"])
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Ensure numeric columns
for col in ["Protein", "Carbs", "Fat", "Calories", "Servings"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Sort by date to fix graph axis issues
df = df.sort_values("Date")

# ---------------------------
# Date Selection
# ---------------------------
st.subheader("Select Date")
selected_date = st.date_input("Pick a date", value=df["Date"].max())
day_df = df[df["Date"] == selected_date]

if day_df.empty:
    st.info("No meals logged for this date.")
    st.stop()

# ---------------------------
# Display Meals Table
# ---------------------------
st.subheader(f"📋 Meals on {selected_date}")
st.dataframe(day_df[["MealType", "Meal", "Servings", "Protein", "Carbs", "Fat", "Calories"]])

# ---------------------------
# Totals
# ---------------------------
total_protein = day_df["Protein"].sum()
total_carbs = day_df["Carbs"].sum()
total_fat = day_df["Fat"].sum()
total_calories = day_df["Calories"].sum()
calorie_goal = st.number_input("Set Daily Calorie Goal", min_value=0, value=2000)
remaining_calories = max(calorie_goal - total_calories, 0)

# ---------------------------------------------------------
# 🔥 CALORIES OVER TIME WITH RANGE SELECTOR 
# ---------------------------------------------------------

st.markdown("---")
st.subheader("📆 Calories Over Time (Select Range)")

range_option = st.selectbox(
    "Select Time Range:",
    [ "Week", "Month", "Year", "Max"],
    index=0
)

today = datetime.now().date()

# ---- RANGE FILTER ----
if range_option == "Day":
    # Filter today's meals
    df_range = df[df["DateTime"].dt.date == today].copy()

    # FIX the broken Jan 01 label by using time instead of date
    if not df_range.empty:
        df_range["TimeOnly"] = df_range["DateTime"].dt.strftime("%I:%M %p")


elif range_option == "Week":
    df_range = df[df["Date"] >= (today - timedelta(days=7))]

elif range_option == "Month":
    df_range = df[df["Date"] >= (today - timedelta(days=30))]

elif range_option == "Year":
    df_range = df[df["Date"] >= (today - timedelta(days=365))]

else:  # Max
    df_range = df.copy()

# ---- CLEAN CALORIES OVER TIME GRAPH ----
if df_range.empty:
    st.info("No data available for this time range.")
else:
    st.write("### 🔥 Calories Over Time")
    fig, ax = plt.subplots(figsize=(7, 3))  # clean compact size

    # Group by date
    calories_daily = df_range.groupby("Date")["Calories"].sum()

    # Convert to datetime for proper plotting
    dates = pd.to_datetime(calories_daily.index)

    # Plot
    ax.plot(
        dates,
        calories_daily.values,
        marker="o",
        linewidth=2,
        color="#66B3FF"
    )

    ax.set_ylabel("Calories")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.3)

    # ---- FIX LABEL FORMATTING ----
    fig.autofmt_xdate(rotation=45)

    # Choose nice date formatting depending on range
    import matplotlib.dates as mdates

    if range_option == "Day":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    elif range_option == "Week":
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    elif range_option == "Month":
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    elif range_option == "Year":
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    else:  # Max
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    fig.tight_layout()
    st.pyplot(fig)


# ---------------------------
# Pie Charts Side by Side
# ---------------------------
st.subheader("🥗 Macronutrients & Calories Overview")
col1, col2 = st.columns(2)

# Pie 1
with col1:
    fig1, ax1 = plt.subplots(figsize=(3,3))  # smaller
    nutrients = pd.Series([total_protein, total_carbs, total_fat], index=["Protein","Carbs","Fat"])
    if nutrients.sum() > 0:
        nutrients.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax1)
        ax1.set_ylabel("")
        ax1.set_title("Macronutrient Distribution")
        fig1.tight_layout()
        st.pyplot(fig1)
    else:
        st.info("No macronutrients recorded for this day.")

# Pie 2
with col2:
    fig2, ax2 = plt.subplots(figsize=(3,3))  # smaller
    cal_data = pd.Series([total_calories, remaining_calories], index=["Consumed","Remaining"])
    if cal_data.sum() > 0:
        cal_data.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax2)
        ax2.set_ylabel("")
        ax2.set_title(f"Calories (Goal: {calorie_goal} kcal)")
        fig2.tight_layout()
        st.pyplot(fig2)
    else:
        st.info("No calories recorded for this day.")

# ---------------------------
# Stacked Bar + Cumulative Line Side by Side
# ---------------------------
st.subheader("📊 Macros by Meal Type & Cumulative Timeline")
col3, col4 = st.columns(2)

# Stacked Bar
with col3:
    meal_totals = day_df.groupby("MealType")[["Protein","Carbs","Fat"]].sum().reset_index()
    if not meal_totals.empty:
        fig3, ax3 = plt.subplots(figsize=(4.5,3))  # slightly smaller
        meal_totals.set_index("MealType")[["Protein","Carbs","Fat"]].plot(
            kind="bar", stacked=True, ax=ax3
        )
        ax3.set_ylabel("Grams")
        ax3.set_title("Macros by Meal Type")
        ax3.legend(fontsize=7)
        fig3.tight_layout()
        st.pyplot(fig3)

# Cumulative Line
with col4:
    day_df_sorted = day_df.sort_values("DateTime").copy()
    day_df_sorted["CumulativeProtein"] = day_df_sorted["Protein"].cumsum()
    day_df_sorted["CumulativeCarbs"] = day_df_sorted["Carbs"].cumsum()
    day_df_sorted["CumulativeFat"] = day_df_sorted["Fat"].cumsum()

    fig4, ax4 = plt.subplots(figsize=(4.5,3))
    ax4.plot(day_df_sorted["DateTime"], day_df_sorted["CumulativeProtein"], marker='o', label="Protein")
    ax4.plot(day_df_sorted["DateTime"], day_df_sorted["CumulativeCarbs"], marker='o', label="Carbs")
    ax4.plot(day_df_sorted["DateTime"], day_df_sorted["CumulativeFat"], marker='o', label="Fat")
    ax4.set_ylabel("Grams")
    ax4.set_title("Cumulative Macronutrients")
    ax4.legend(fontsize=7)
    fig4.tight_layout()
    st.pyplot(fig4)

# ---------------------------
# Horizontal Stacked Bar: Macro Proportions
# ---------------------------
st.subheader("📊 Macro Proportions")
fig5, ax5 = plt.subplots(figsize=(5,1.2))
macro_props = pd.DataFrame({
    "Protein":[total_protein],
    "Carbs":[total_carbs],
    "Fat":[total_fat]
})
macro_props.plot(kind="barh", stacked=True, ax=ax5)
ax5.set_xlabel("Grams")
ax5.set_ylabel("")
ax5.set_title("Macro Proportion (Horizontal)")
ax5.legend(fontsize=7)
fig5.tight_layout()
st.pyplot(fig5)
