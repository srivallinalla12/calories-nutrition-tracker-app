import pandas as pd

# Load the sample dataset
meals = pd.read_csv("/Users/sulavbista/Desktop/Fall 2025/CIS 485 /calories-nutrition-tracker-app/data/meals.csv")

print("****** Weight Loss | High Protein | Balanced Diet ******")

user_goals = input("What is your goal?\nAnswer: ").strip().lower()

while user_goals != "bye":

    if user_goals == "weight loss":
        print("\nYour meal plan for today (Weight Loss):")
        all_meals = pd.DataFrame()

        for cat in ["Breakfast", "Lunch", "Dinner"]:
            filtered = meals[(meals["Category"] == cat) & (meals["Calories"] <= 400)]
            if not filtered.empty:
                meal_choice = filtered.sample(1)
                all_meals = pd.concat([all_meals, meal_choice[["Meal", "Calories"]]])
            else:
                print(f"No {cat} meals found for this goal.")

        if not all_meals.empty:
            print(all_meals.to_string(index=False))

    elif user_goals == "high protein":
        print("\nYour meal plan for today (High Protein):")
        all_meals = pd.DataFrame()

        for cat in ["Breakfast", "Lunch", "Dinner"]:
            filtered = meals[(meals["Category"] == cat) & (meals["Protein"] >= 25)]
            if not filtered.empty:
                meal_choice = filtered.sample(1)
                all_meals = pd.concat([all_meals, meal_choice[["Meal", "Calories", "Protein"]]])
            else:
                print(f"No {cat} meals found for this goal.")

        if not all_meals.empty:
            print(all_meals.to_string(index=False))

    elif user_goals == "balanced diet":
        print("\nYour meal plan for today (Balanced Diet):")
        all_meals = pd.DataFrame()

        for cat in ["Breakfast", "Lunch", "Dinner"]:
            filtered = meals[(meals["Category"] == cat) &
                             (meals["Calories"].between(350, 500)) &
                             (meals["Protein"].between(15, 30)) &
                             (meals["Fat"].between(8, 15))]
            if not filtered.empty:
                meal_choice = filtered.sample(1)
                all_meals = pd.concat([all_meals, meal_choice[["Meal", "Calories", "Protein", "Fat"]]])
            else:
                print(f"No {cat} meals found for this goal.")

        if not all_meals.empty:
            print(all_meals.to_string(index=False))

    else:
        print("More features coming. Try next time!")

    user_goals = input("\nWhat is your goal? (Type 'Bye' to exit)\nAnswer: ").strip().lower()
