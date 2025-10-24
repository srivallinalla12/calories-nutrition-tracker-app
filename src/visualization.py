import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def show_pie_chart(df):
    totals = df[["carbs", "protein", "fat"]].sum().fillna(0)  # Replace NaN with 0
    if totals.sum() == 0:
        st.info("No nutrient data available yet to plot a pie chart.")
        return
    
    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct="%1.1f%%")
    ax.set_title("Total Nutrients Breakdown")
    st.pyplot(fig)

def show_calorie_trend(df):
    df["date_logged"] = pd.to_datetime(df["date_logged"])
    daily_calories = df.groupby("date_logged")["calories"].sum()
    if daily_calories.empty:
        st.info("No calorie data available yet to show trend.")
        return
    st.line_chart(daily_calories)

def show_bar_chart(df):
    nutrients = df[["carbs", "protein", "fat"]].sum().fillna(0)
    if nutrients.sum() == 0:
        st.info("No nutrient data available yet to show bar chart.")
        return
    st.bar_chart(nutrients)
