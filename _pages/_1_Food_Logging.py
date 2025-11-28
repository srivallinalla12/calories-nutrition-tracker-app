import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

def food_logging_page():

    # ---------------------------
    # SESSION CHECK
    # ---------------------------
    if "user" not in st.session_state or st.session_state["user"] is None:
        st.warning("Please log in first to access this page.")
        return

    username = st.session_state["user"]  # <-- CURRENT LOGGED USER

    st.title("📊 Food Log")

    # ---------------------------
    # USER-SPECIFIC PATHS
    # ---------------------------
    DATA_DIR = "data"

    # Demo user keeps the shared meals.csv
    if username == "demo":
        MEALS_FILE = os.path.join(DATA_DIR, "meals.csv")
    else:
        MEALS_FILE = os.path.join(DATA_DIR, f"{username}_meals.csv")

    USDA_FILE = "USDA.csv"

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    expected_cols = ["DateTime", "Date", "MealType", "Meal",
                     "Servings", "Calories", "Protein", "Carbs", "Fat"]

    # Ensure user meals file exists
    if not os.path.exists(MEALS_FILE) or os.stat(MEALS_FILE).st_size == 0:
        pd.DataFrame(columns=expected_cols).to_csv(MEALS_FILE, index=False)

    # ---------------------------
    # Load USDA
    # ---------------------------
    if not os.path.exists(USDA_FILE):
        st.error("Missing USDA.csv. Please place it in the main folder.")
        st.stop()

    meals_df = pd.read_csv(USDA_FILE)
    meals_df = meals_df.rename(columns={"Description": "Meal", "Carbohydrate": "Carbs"})
    for col in ["Calories", "Protein", "Carbs", "Fat"]:
        meals_df[col] = pd.to_numeric(meals_df[col], errors="coerce")

    # Meal Name Cleanup
    def get_display_name(desc):
        if pd.isna(desc):
            return "Unknown"
        desc = str(desc).lower()
        if "rice" in desc:
            if "brown" in desc:
                return "Brown Rice"
            elif "wild" in desc:
                return "Wild Rice"
            return "White Rice"
        if "chick" in desc:
            return "Chicken"
        if "tomato" in desc:
            return "Tomato"
        if "butter" in desc:
            return "Butter"
        if "milk" in desc:
            return "Milk"
        if "soup" in desc:
            if "tomato" in desc:
                return "Tomato Soup"
            if "chick" in desc:
                return "Chicken Soup"
        return str(desc).split(",")[0].title()

    meals_df["DisplayMeal"] = meals_df["Meal"].apply(get_display_name)

    friendly_df = meals_df.groupby("DisplayMeal").agg({
        "Calories": "mean",
        "Protein": "mean",
        "Carbs": "mean",
        "Fat": "mean"
    }).reset_index()

    # ---------------------------
    # Helper functions NOW use user-specific files
    # ---------------------------
    def read_meals_file():
        df = pd.read_csv(MEALS_FILE)
        for col in expected_cols:
            if col not in df.columns:
                df[col] = pd.NA
        for col in ["Servings", "Calories", "Protein", "Carbs", "Fat"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df[expected_cols]

    def write_meals_file(df):
        df.to_csv(MEALS_FILE, index=False)

    # ---------------------------
    # Session State
    # ---------------------------
    username = st.session_state["user"]
    if "meals_by_date" not in st.session_state:
        st.session_state.meals_by_date = {}

    # ---------------------------
    # Page Title & Date
    # ---------------------------
    st.title("🍽️ Food Logging (Friendly USDA Dataset)")
    selected_date = st.date_input("Select a date to view/edit meals", value=date.today())
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    # Load meals
    # Ensure each user has their own namespace
    if username not in st.session_state.meals_by_date:
        st.session_state.meals_by_date[username] = {}

    # Load meals for selected date
    all_meals_df = read_meals_file()
    user_meals_by_date = st.session_state.meals_by_date[username]

    if selected_date_str not in user_meals_by_date:
        user_meals_by_date[selected_date_str] = all_meals_df[all_meals_df["Date"] == selected_date_str].to_dict("records")

    today_meals = user_meals_by_date[selected_date_str]
    # ---------------------------
    # Meal Input
    # ---------------------------
    st.subheader("Add a Meal")
    meal_input = st.text_input("Search Meal", placeholder="Type to search...")
    selected_meal = None
    matched_meals = pd.DataFrame()

    if meal_input.strip():
        matched_meals = friendly_df[friendly_df["DisplayMeal"]
                                    .str.contains(meal_input, case=False, na=False)]
        if not matched_meals.empty:
            option = st.selectbox("Select Meal", matched_meals["DisplayMeal"].tolist())
            if option:
                selected_meal = matched_meals[matched_meals["DisplayMeal"] == option].iloc[0]

    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    servings = st.number_input("Servings", min_value=0.1, value=1.0, step=0.1)

    # Autofill macros
    if selected_meal is not None:
        calories = selected_meal["Calories"] * servings
        protein = selected_meal["Protein"] * servings
        carbs = selected_meal["Carbs"] * servings
        fat = selected_meal["Fat"] * servings
        st.info(f"Calories: {calories:.1f} kcal | Protein: {protein:.1f} g | Carbs: {carbs:.1f} g | Fat: {fat:.1f} g")
    else:
        calories = st.number_input("Calories", min_value=0.0, value=0.0)
        protein = st.number_input("Protein", min_value=0.0, value=0.0)
        carbs = st.number_input("Carbs", min_value=0.0, value=0.0)
        fat = st.number_input("Fat", min_value=0.0, value=0.0)

    # ---------------------------
    # Add Meal Button
    # ---------------------------
    if st.button("➕ Add Meal"):
        if selected_meal is None:
            st.warning("Please select a meal from the list.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            row = {
                "DateTime": timestamp,
                "Date": selected_date_str,
                "MealType": meal_type,
                "Meal": selected_meal["DisplayMeal"],
                "Servings": float(servings),
                "Calories": float(calories),
                "Protein": float(protein),
                "Carbs": float(carbs),
                "Fat": float(fat)
            }

            # Add to session
            st.session_state.meals_by_date.setdefault(selected_date_str, []).append(row)

            # Write to user-specific CSV
            all_meals_df = read_meals_file()
            all_meals_df = pd.concat([all_meals_df, pd.DataFrame([row])], ignore_index=True)
            write_meals_file(all_meals_df)

            st.success(f"{meal_type} - {selected_meal['DisplayMeal']} added!")

    # ---------------------------
    # Display Meals (Edit/Delete)
    # ---------------------------
    if today_meals:
        st.subheader(f"📋 Meals Logged on {selected_date_str}")
        st.markdown("---")
        order = ["Breakfast", "Lunch", "Dinner", "Snack"]

        for m_type in order:
            meals = [m for m in today_meals if m["MealType"] == m_type]
            if meals:
                st.markdown(f"### {m_type}")
                for idx, row in enumerate(meals):
                    edit_key = f"edit_{m_type}_{idx}_{selected_date_str}"
                    save_key = f"save_{m_type}_{idx}_{selected_date_str}"
                    delete_key = f"delete_{m_type}_{idx}_{selected_date_str}"

                    if st.session_state.get(edit_key, False):
                        col1, col2, col3, col4, col5, col6, col7 = st.columns([3,1,1,1,1,1,1])
                        col1.write(row["Meal"])
                        servings = col2.number_input("Servings", min_value=0.1, value=row["Servings"], step=0.1, key=f"servings_{idx}_{selected_date_str}")
                        calories = col3.number_input("Calories", min_value=0.0, value=row["Calories"], step=0.1, key=f"cal_{idx}_{selected_date_str}")
                        protein = col4.number_input("Protein", min_value=0.0, value=row["Protein"], step=0.1, key=f"protein_{idx}_{selected_date_str}")
                        carbs = col5.number_input("Carbs", min_value=0.0, value=row["Carbs"], step=0.1, key=f"carbs_{idx}_{selected_date_str}")
                        fat = col6.number_input("Fat", min_value=0.0, value=row["Fat"], step=0.1, key=f"fat_{idx}_{selected_date_str}")

                        if col7.button("💾 Save", key=save_key):
                            st.session_state.meals_by_date[selected_date_str][idx] = {
                                "DateTime": row["DateTime"],
                                "Date": selected_date_str,
                                "MealType": m_type,
                                "Meal": row["Meal"], 
                                "Servings": servings,
                                "Calories": calories,
                                "Protein": protein,
                                "Carbs": carbs,
                                "Fat": fat
                            }
                            updated_df = pd.DataFrame(st.session_state.meals_by_date[selected_date_str])
                            all_meals_df = read_meals_file()
                            all_meals_df = all_meals_df[all_meals_df["Date"] != selected_date_str]
                            all_meals_df = pd.concat([all_meals_df, updated_df], ignore_index=True)
                            write_meals_file(all_meals_df)
                            st.session_state[edit_key] = False
                            st.experimental_rerun()

                    else:
                        col1, col2, col3, col4, col5, col6, col7 = st.columns([3,1,1,1,1,1,1])
                        col1.markdown(f"**{row['Meal']}**")
                        col2.write(row["Servings"])
                        col3.write(f"{row['Calories']:.1f}")
                        col4.write(f"{row['Protein']:.1f}")
                        col5.write(f"{row['Carbs']:.1f}")
                        col6.write(f"{row['Fat']:.1f}")

                        if col7.button("✏️ Edit", key=edit_key):
                            st.session_state[edit_key] = True
                            st.experimental_rerun()

                        if col7.button("🗑️ Delete", key=delete_key):
                            st.session_state.meals_by_date[selected_date_str].pop(idx)
                            updated_df = pd.DataFrame(st.session_state.meals_by_date[selected_date_str])
                            all_meals_df = read_meals_file()
                            all_meals_df = all_meals_df[all_meals_df["Date"] != selected_date_str]
                            all_meals_df = pd.concat([all_meals_df, updated_df], ignore_index=True)
                            write_meals_file(all_meals_df)
                            st.experimental_rerun()
