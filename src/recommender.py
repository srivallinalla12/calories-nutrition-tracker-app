def simple_recommendation(df):
    if df.empty:
        return "Log your meals to get personalized suggestions."
    
    totals = df[["carbs", "protein", "fat"]].sum()
    suggestions = []
    
    if totals["protein"] < 50:
        suggestions.append("Consider adding more protein (e.g., eggs, beans, paneer).")
    if totals["carbs"] > 250:
        suggestions.append("You might want to cut down on carbs (rice, bread).")
    if totals["fat"] > 70:
        suggestions.append("Reduce high-fat foods (fried snacks, butter).")
    
    return " ".join(suggestions) if suggestions else "Your diet looks balanced today!"
