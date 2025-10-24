import pandas as pd
import os
from datetime import date

LOG_FILE = "data/food_log.csv"

def load_food_log():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        return pd.read_csv(LOG_FILE)
    else:
        # Return empty DataFrame with proper headers
        return pd.DataFrame(columns=["food_name", "calories", "carbs", "protein", "fat", "date_logged"])

def add_food_log(food_name, calories, carbs, protein, fat):
    df = load_food_log()
    new_row = {
        "food_name": food_name,
        "calories": calories,
        "carbs": carbs,
        "protein": protein,
        "fat": fat,
        "date_logged": date.today()
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
