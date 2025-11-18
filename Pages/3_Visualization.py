import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📅 Visualization")

df = pd.read_csv("data/meals.csv")

if df.empty:
    st.warning("No data to visualize yet.")
else:
    st.write("### Nutrient Breakdown")
    fig, ax = plt.subplots()
    df[["Protein", "Carbs", "Fat"]].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)
