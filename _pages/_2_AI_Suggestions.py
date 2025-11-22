# _2_AI_Suggestions.py
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def ai_suggestions_page():
    # ---------------------------
    # SESSION CHECK
    # ---------------------------
    if "user" not in st.session_state or st.session_state["user"] is None:
        st.warning("Please log in first to access this page.")
        return

    st.title("💡 AI Nutrition & Calorie Tracker")

    # ---------------------------
    # LOAD USDA DATASET
    # ---------------------------
    meals_file = "USDA.csv"
    meals = pd.read_csv(meals_file)

    meals = meals.rename(columns={
        "Description": "Meal",
        "Carbohydrate": "Carbs"
    })

    for col in ["Calories", "Protein", "Fat", "Carbs"]:
        meals[col] = pd.to_numeric(meals[col], errors="coerce")

    # Simplify common names from Dataset
    def get_display_name(desc):
        desc = desc.lower()
        if "rice" in desc:
            if "brown" in desc:
                return "Brown Rice"
            elif "wild" in desc:
                return "Wild Rice"
            return "White Rice"
        if "chick" in desc:
            return "Chicken"
        if "cheese" in desc:
            return "Cheese"
        if "butter" in desc:
            return "Butter"
        return desc.split(",")[0].title()

    meals["DisplayMeal"] = meals["Meal"].apply(get_display_name)

    # CATEGORIZE FOOD BASED ON BREAKFAST, LUNCH AND DINNER
    def smart_category(row):
        cal = row["Calories"]
        protein = row["Protein"]
        fat = row["Fat"]

        # Breakfast: light, low fat
        if cal <= 450 and fat <= 25:
            return "Breakfast"

        # Lunch: moderate calories
        if 300 <= cal <= 700 and fat <= 40:
            return "Lunch"

        # Dinner: heavier and protein rich
        if cal >= 350 and protein >= 15:
            return "Dinner"

        # Fallback
        return "Lunch"

    meals["Category"] = meals.apply(smart_category, axis=1)

    required = ["Breakfast", "Lunch", "Dinner"]
    existing = meals["Category"].unique().tolist()
    missing = [c for c in required if c not in existing]

    if missing:
        for i, cat in enumerate(missing):
            meals.loc[meals.index[i], "Category"] = cat

    # Summaries
    meal_summary = meals.groupby("DisplayMeal").agg({
        "Calories": "mean",
        "Protein": "mean",
        "Carbs": "mean",
        "Fat": "mean",
        "Category": "first"
    }).reset_index()

    # ---------------------------
    # USER GOAL
    # ---------------------------
    user_goal = st.selectbox(
        "Select your goal:",
        ["Select...", "Weight Loss", "High Protein", "Calorie-Based Plan"]
    )

    # ---------------------------
    # MEAL PLAN GENERATOR
    # ---------------------------
    def choose_meal(category, condition):
        df = meal_summary[meal_summary["Category"] == category]
        df = df[df.apply(condition, axis=1)]
        return df.sample(1).iloc[0] if not df.empty else None

    if user_goal != "Select...":
        st.subheader(f"🍽️ Recommended Meal Plan ({user_goal})")

        # CALORIE-BASED PLAN
        if user_goal == "Calorie-Based Plan":
            target = st.number_input(
                "Enter your daily calorie goal (kcal):",
                min_value=1000, max_value=4000, value=1900
            )

            if st.button("Generate Plan"):
                categories = ["Breakfast", "Lunch", "Dinner"]
                total_cal = 0
                output = []

                # New balanced distribution
                weights = {
                    "Breakfast": 0.30,
                    "Lunch": 0.40,
                    "Dinner": 0.30
                }

                for cat in categories:
                    allowed_cal = target * weights[cat]

                    # Pick meal closest to allowed calories
                    df = meal_summary[meal_summary["Category"] == cat]
                    df["cal_diff"] = (df["Calories"] - allowed_cal).abs()
                    meal = df.sort_values("cal_diff").iloc[0]

                    total_cal += meal["Calories"]
                    output.append(
                        f"**{cat}:** {meal['DisplayMeal']} — {meal['Calories']:.0f} kcal"
                    )

                st.markdown("\n".join(output))
                st.success(f"Total for the day: **{total_cal:.0f} kcal** (Target: {target})")

        # WEIGHT LOSS / HIGH PROTEIN
        else:
            if user_goal == "Weight Loss":
                for cat in ["Breakfast", "Lunch", "Dinner"]:
                    df = meal_summary[
                        (meal_summary["Category"] == cat) &
                        (meal_summary["Calories"] <= 400)
                    ]

                    if df.empty and cat == "Dinner":
                        df = meal_summary[meal_summary["Category"] == cat]

                    if df.empty:
                        st.warning(f"No meals found for {cat}.")
                        continue

                    selected = df.sample(min(2, len(df)))
                    for _, meal in selected.iterrows():
                        st.markdown(
                            f"**{cat}:** {meal['DisplayMeal']} — "
                            f"{meal['Calories']:.0f} kcal, "
                            f"{meal['Protein']:.1f}g protein"
                        )

            elif user_goal == "High Protein":
                condition = lambda row: row["Protein"] >= 10
                for cat in ["Breakfast", "Lunch", "Dinner"]:
                    meal = choose_meal(cat, condition)
                    if meal is not None:
                        st.markdown(
                            f"**{cat}:** {meal['DisplayMeal']} — {meal['Calories']:.0f} kcal, "
                            f"{meal['Protein']:.1f}g protein"
                        )
                    else:
                        st.warning(f"No meals found for {cat}.")
    else:
        st.info("Please select your goal.")

    # ---------------------------
    # CHATBOT
    # ---------------------------
    st.markdown("---")
    st.subheader("🤖 AI Assistant")

    chat_meals = meal_summary.head(50).to_dict(orient="records")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def is_unhealthy_prompt(user_input):
        bad = [
            "500 calories", "starve", "skip meals",
            "lose 10 lbs in 3 days", "fasting for days"
        ]
        return any(x in user_input.lower() for x in bad)

    def ask_gpt(user_input):
        if is_unhealthy_prompt(user_input):
            return "⚠️ I cannot give extreme dieting advice."

        system_prompt = f"""
        You are an AI Assistant, a friendly nutrition assistant.
        Only use this dataset when giving food suggestions:
        {chat_meals}
        """

        messages = [{"role": "system", "content": system_prompt}]
        messages += st.session_state.chat_history
        messages.append({"role": "user", "content": user_input})

        reply = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=250,
            temperature=0.6
        )

        return reply.choices[0].message.content.strip()

    # QUICK ASK BUTTONS
    st.write("Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🥗 Low-Carb Meals"):
            msg = "Show me meals with less than 20g carbs."
            st.session_state.chat_history.append({"role":"user","content":msg})
            st.session_state.chat_history.append(
                {"role":"assistant","content":ask_gpt(msg)}
            )

    with col2:
        if st.button("🥤 Low-Fat Meals"):
            msg = "Show me meals with less than 10g fat."
            st.session_state.chat_history.append({"role":"user","content":msg})
            st.session_state.chat_history.append(
                {"role":"assistant","content":ask_gpt(msg)}
            )

    with col3:
        if st.button("💪 High-Protein Meals"):
            msg = "Show me meals with more than 25g protein."
            st.session_state.chat_history.append({"role":"user","content":msg})
            st.session_state.chat_history.append(
                {"role":"assistant","content":ask_gpt(msg)}
            )

    # SHOW CHAT HISTORY
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    # USER CHAT INPUT
    if user_msg := st.chat_input("Ask anything..."):
        st.chat_message("user").write(user_msg)
        st.session_state.chat_history.append({"role":"user","content":user_msg})
        bot = ask_gpt(user_msg)
        st.session_state.chat_history.append({"role":"assistant","content":bot})
        st.chat_message("assistant").write(bot)
