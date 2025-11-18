import streamlit as st
import pandas as pd
from datetime import datetime, date

st.title("🍽️ Food Logging (Friendly USDA Dataset)")

# --- Load USDA dataset ---
meals_file = "USDA.csv"
meals_df = pd.read_csv(meals_file)

# Rename columns for consistency
meals_df = meals_df.rename(columns={
    "Description": "Meal",
    "Carbohydrate": "Carbs"
})

# Convert numeric columns
for col in ["Calories", "Protein", "Carbs", "Fat"]:
    meals_df[col] = pd.to_numeric(meals_df[col], errors="coerce")

# --- Create friendly display names ---
def get_display_name(desc):
    desc = desc.lower()
    if "rice" in desc:
        if "brown" in desc:
            return "Brown Rice"
        elif "wild" in desc:
            return "Wild Rice"
        return "White Rice"
    if "chick" in desc or "chicken" in desc:
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
        elif "chick" in desc:
            return "Chicken Soup"
    return desc.split(",")[0].title()

meals_df["DisplayMeal"] = meals_df["Meal"].apply(get_display_name)

# Group by friendly name and average macros
friendly_df = meals_df.groupby("DisplayMeal").agg({
    "Calories": "mean",
    "Protein": "mean",
    "Carbs": "mean",
    "Fat": "mean"
}).reset_index()

# --- Session storage ---
if "today_meals" not in st.session_state:
    st.session_state.today_meals = []

# --- Meal Input Section ---
st.subheader("Add a Meal")

meal_input = st.text_input("Search Meal", placeholder="Start typing to search...")

# Filter meals for autocomplete
matched_meals = friendly_df[friendly_df["DisplayMeal"].str.contains(meal_input, case=False, na=False)]

selected_meal = None
if not matched_meals.empty and meal_input != "":
    option = st.selectbox("Select a Meal", matched_meals["DisplayMeal"].tolist())
    if option:
        selected_meal = friendly_df[friendly_df["DisplayMeal"] == option].iloc[0]

# Meal type and servings
meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
servings = st.number_input("Number of servings", min_value=0.1, value=1.0, step=0.1)

# Autofill macros if meal selected
if selected_meal is not None:
    calories = selected_meal["Calories"] * servings
    protein = selected_meal["Protein"] * servings
    carbs = selected_meal["Carbs"] * servings
    fat = selected_meal["Fat"] * servings
    st.info(f"Calories: {calories:.1f} kcal | Protein: {protein:.1f} g | Carbs: {carbs:.1f} g | Fat: {fat:.1f} g")
else:
    calories = st.number_input("Calories (kcal)", min_value=0)
    protein = st.number_input("Protein (g)", min_value=0)
    carbs = st.number_input("Carbs (g)", min_value=0)
    fat = st.number_input("Fat (g)", min_value=0)

# Add meal to session
if st.button("➕ Add Meal"):
    if meal_input.strip() == "":
        st.warning("Please enter a meal name.")
    else:
        st.session_state.today_meals.append({
            "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "MealType": meal_type,
            "Meal": meal_input.strip(),
            "Servings": servings,
            "Calories": calories,
            "Protein": protein,
            "Carbs": carbs,
            "Fat": fat
        })
        st.success(f"{meal_type} - {meal_input} ({servings} servings) added!")

# --- Display today's meals grouped by type ---
if st.session_state.today_meals:
    st.markdown("---")
    st.subheader(f"📋 Meals Logged Today ({date.today()})")
    
    meal_types_order = ["Breakfast", "Lunch", "Dinner", "Snack"]
    
    for m_type in meal_types_order:
        meals_of_type = [m for m in st.session_state.today_meals if m["MealType"] == m_type]
        if meals_of_type:
            st.markdown(f"### {m_type}")
            for i, row in enumerate(meals_of_type):
                col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
                col1.markdown(f"**{row['Meal']}**")
                col2.write(f"{row['Servings']}")
                col3.write(f"{row['Calories']:.1f}")
                col4.write(f"{row['Protein']:.1f}")
                col5.write(f"{row['Carbs']:.1f}")
                
                edit_col, delete_col = st.columns([1, 1])
                
                # Edit
                if edit_col.button("✏️", key=f"edit_{m_type}_{i}"):
                    with st.form(key=f"edit_form_{m_type}_{i}"):
                        meal_name_edit = st.text_input("Meal Name", value=row["Meal"])
                        servings_edit = st.number_input("Number of servings", min_value=0.1, value=row["Servings"], step=0.1)
                        if st.form_submit_button("💾 Save Changes"):
                            idx_in_session = st.session_state.today_meals.index(row)
                            st.session_state.today_meals[idx_in_session]["Meal"] = meal_name_edit
                            st.session_state.today_meals[idx_in_session]["Servings"] = servings_edit
                            st.session_state.today_meals[idx_in_session]["Calories"] = row["Calories"] / row["Servings"] * servings_edit
                            st.session_state.today_meals[idx_in_session]["Protein"] = row["Protein"] / row["Servings"] * servings_edit
                            st.session_state.today_meals[idx_in_session]["Carbs"] = row["Carbs"] / row["Servings"] * servings_edit
                            st.session_state.today_meals[idx_in_session]["Fat"] = row["Fat"] / row["Servings"] * servings_edit
                            st.success("Changes saved!")
                
                # Delete
                if delete_col.button("🗑️", key=f"del_{m_type}_{i}"):
                    idx_in_session = st.session_state.today_meals.index(row)
                    st.session_state.today_meals.pop(idx_in_session)
                    st.success(f"Deleted {row['Meal']}")

            st.markdown("---")  # line between meal types

    # --- Nutrient summary ---
    st.markdown("### 🧮 Total Nutrients Today")
    today_df = pd.DataFrame(st.session_state.today_meals)
    st.write(f"Calories: {today_df['Calories'].sum():.1f} kcal")
    st.write(f"Protein: {today_df['Protein'].sum():.1f} g")
    st.write(f"Carbs: {today_df['Carbs'].sum():.1f} g")
    st.write(f"Fat: {today_df['Fat'].sum():.1f} g")
