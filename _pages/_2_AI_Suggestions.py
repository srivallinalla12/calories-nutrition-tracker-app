# _2_AI_Suggestions.py
import streamlit as st 
import pandas as pd 
import os 
from datetime import datetime 
from dotenv import load_dotenv
from openai import OpenAI 

# -----------------------
# LOAD ENV
# -----------------------
load_dotenv()
client_gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  

def ai_suggestions_page():
    # -----------------------
    # SESSION CHECK
    # -----------------------
    if "user" not in st.session_state or st.session_state["user"] is None:
        st.warning("Please log in first to access this page.")
        st.stop()  # stops script until login

    st.title("💡 AI Nutrition & Calorie Tracker")

    # -----------------------
    # LOAD USDA DATASET
    # -----------------------
    usda_file = "USDA.csv"
    usda_meals = pd.read_csv(usda_file)

    usda_meals = usda_meals.rename(columns={
        "Description": "Meal",
        "Carbohydrate": "Carbs"
    })

    for col in ["Calories", "Protein", "Fat", "Carbs"]:
        usda_meals[col] = pd.to_numeric(usda_meals[col], errors="coerce")

    # Remove junk/processed foods
    junk_keywords = [
        "candy", "toffee", "syrup", "sugar", "frosting", "gelatin",
        "powder", "mix", "drink", "beverage", "jelly", "dessert",
        "cookie", "cake", "brownie", "marshmallow", "gum", "cola",
        "chewing", "pudding", "cream", "whipped", "ice cream",
        "liver", "sausage", "paste", "hot dog", "corn syrup",
        "oil spray", "shortening", "margarine", "oleo", "yeast extract",
        "gel", "flavoring", "confection", "capsule", "tablet", "supplement"
    ]

    def is_junk_or_weird(meal_name):
        meal = meal_name.lower()
        return any(j in meal for j in junk_keywords)

    usda_meals = usda_meals[~usda_meals["Meal"].apply(is_junk_or_weird)]

    # Simplify names
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

    usda_meals["DisplayMeal"] = usda_meals["Meal"].apply(get_display_name)

    # Categorize
    def smart_category(row):
        cal = row["Calories"]
        protein = row["Protein"]
        fat = row["Fat"]
        if cal <= 450 and fat <= 25:
            return "Breakfast"
        if 300 <= cal <= 700 and fat <= 40:
            return "Lunch"
        if cal >= 350 and protein >= 15:
            return "Dinner"
        return "Lunch"

    usda_meals["Category"] = usda_meals.apply(smart_category, axis=1)

    meal_summary_usda = usda_meals.groupby("DisplayMeal").agg({
        "Calories": "mean",
        "Protein": "mean",
        "Carbs": "mean",
        "Fat": "mean",
        "Category": "first"
    }).reset_index()

    # -----------------------
    # LOAD HEALTHY MEALS DATASET
    # -----------------------
    healthy_file = "healthy_meals.csv"
    healthy = pd.read_csv(healthy_file)

    if "DisplayMeal" in healthy.columns and "Meal" not in healthy.columns:
        healthy = healthy.rename(columns={"DisplayMeal": "Meal"})

    for col in ["Calories", "Protein", "Carbs", "Fat"]:
        if col in healthy.columns:
            healthy[col] = pd.to_numeric(healthy[col], errors="coerce")
        else:
            healthy[col] = pd.NA

    healthy = healthy.dropna(subset=["Category", "Meal"]).reset_index(drop=True)
    healthy["Category"] = healthy["Category"].str.title().str.strip()

    # -----------------------
    # GOAL SELECTION BUTTONS
    # -----------------------
    st.subheader("Select Your Goal")

    if "user_goal" not in st.session_state:
        st.session_state.user_goal = None

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🥗 Weight Loss"):
            st.session_state.user_goal = "Weight Loss"
    with col2:
        if st.button("💪 High Protein"):
            st.session_state.user_goal = "High Protein"
    with col3:
        if st.button("🔥 Calorie-Based Plan"):
            st.session_state.user_goal = "Calorie-Based Plan"

    user_goal = st.session_state.user_goal

    # -----------------------
    # HELPER FUNCTION
    # -----------------------
    def choose_meal(df, category, condition):
        df_cat = df[df["Category"] == category]
        df_cat = df_cat[df_cat.apply(condition, axis=1)]
        return df_cat.sample(1).iloc[0] if not df_cat.empty else None

    # -----------------------
    # MEAL PLAN GENERATION
    # -----------------------
    if user_goal:
        st.subheader(f"🍽️ Recommended Meal Plan ({user_goal})")

        if user_goal == "Calorie-Based Plan":
            if "generate_plan" not in st.session_state:
                st.session_state.generate_plan = False

            target = st.number_input(
                "Enter your daily calorie goal (kcal):",
                min_value=1000, max_value=4000, value=1900
            )

            if st.button("Generate Plan"):
                st.session_state.generate_plan = True

            if st.session_state.generate_plan:
                categories = ["Breakfast", "Lunch", "Dinner"]
                total_cal = 0
                output = []

                weights = {"Breakfast": 0.30, "Lunch": 0.40, "Dinner": 0.30}

                for cat in categories:
                    allowed_cal = target * weights[cat]
                    df = healthy[healthy["Category"] == cat].copy()
                    df["cal_diff"] = (df["Calories"] - allowed_cal).abs()
                    if df.empty:
                        st.warning(f"No healthy meals for {cat}.")
                        continue
                    meal = df.sort_values("cal_diff").iloc[0]
                    total_cal += meal["Calories"]
                    output.append(
                        f"**{cat}:** {meal['Meal']} — {meal['Calories']:.0f} kcal"
                    )

                st.markdown("\n".join(output))
                st.success(f"Total for the day: **{total_cal:.0f} kcal** (Target: {target})")

        elif user_goal == "Weight Loss":
            for cat in ["Breakfast", "Lunch", "Dinner"]:
                df = healthy[(healthy["Category"] == cat) & (healthy["Calories"] <= 400)]
                if df.empty:
                    df = healthy[healthy["Category"] == cat]
                if df.empty:
                    st.warning(f"No healthy meals found for {cat}.")
                    continue
                selected = df.sample(min(2, len(df)))
                for _, meal in selected.iterrows():
                    st.markdown(
                        f"**{cat}:** {meal['Meal']} — {meal['Calories']:.0f} kcal, {meal['Protein']:.1f}g protein"
                    )

        elif user_goal == "High Protein":
            condition = lambda row: row["Protein"] >= 20
            for cat in ["Breakfast", "Lunch", "Dinner"]:
                meal = choose_meal(healthy, cat, condition)
                if meal is not None:
                    st.markdown(
                        f"**{cat}:** {meal['Meal']} — {meal['Calories']:.0f} kcal, {meal['Protein']:.1f}g protein"
                    )
                else:
                    st.warning(f"No healthy meals found for {cat}.")

    # -----------------------
    # CHATBOT
    # -----------------------
    st.markdown("---")
    st.subheader("🤖 AI Assistant")

    chat_meals = meal_summary_usda.head(50).to_dict(orient="records")

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
        You are a smart, friendly nutrition assistant (like ChatGPT).
        Use the following dataset only as reference, but do not blindly suggest items.
        Instructions for giving advice:
        - Prefer healthy and balanced meals.
        - Combine items into realistic breakfast, lunch, and dinner meals.
        - Adjust portion sizes if needed (e.g., 2 pieces of candy as a snack).
        - Provide calories, protein, carbs, and fat for each meal or snack.
        - Avoid extreme diets, skipping meals, or unhealthy combinations.
        - Give practical advice on what to pair with the food.
        Dataset:
        {chat_meals}
        """

        messages = [{"role": "system", "content": system_prompt}]
        messages += st.session_state.chat_history
        messages.append({"role": "user", "content": user_input + 
                        "\nPlease make your suggestions realistic and balanced."})

        reply = client_gpt.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )

        return reply.choices[0].message.content.strip()

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
