# ⭐ Calorie & Nutrition Tracking App 

A personalized nutrition-tracking web application built with **Python**, **Streamlit**, and **Pandas**, featuring **AI-powered meal suggestions**, daily food logging, macro visualization, and user-specific data storage.

Designed to help users track calories, improve diet habits, and receive targeted meal recommendations for **weight loss, maintenance, or muscle gain**.

---

## 🚀 Features

### 🔐 1. Secure Login & Session Management
- Each user gets a unique session using `st.session_state["user"]`.
- Personalized meal logs are stored under the user’s own CSV file:
- Demo user support included.

---

### 🍽️ 2. Meal Logging System
Users can log meals with the following details:
- Calories  
- Protein  
- Carbs  
- Fat  
- Date  

Real-time updates using `st.rerun()` for:
- Adding meals  
- Editing meals  
- Deleting meals  

Data stored dynamically in both:
- Session state  
- User-specific CSV  

---

### 🤖 3. AI Meal Recommendations
Smart meal suggestions powered by an AI model built around:
- Target calorie input  
- User goal (Weight Loss / Maintenance / Weight Gain)  
- Vegetarian / Non-Veg preference  

AI generates balanced meal ideas based on:
- Calorie density  
- Macro structure  
- Weight-management strategy  

**Examples:**
- **Weight Loss →** high-protein, low-calorie meals  
- **Weight Gain →** high-calorie, nutrient-dense meals  
- **Balanced →** controlled macros matched to calorie target  

---

### 📊 4. Interactive Nutrition Visualization
Users can view trends over time for:
- Total Calories  
- Protein Intake  
- Carbs  
- Fat  

Includes:
- Daily aggregation  
- Clean data validation  
- Dynamic Streamlit charts  

Helps users understand dietary patterns and make informed adjustments.

---

## 🧱 5. Modular Application Architecture

### 📂 Project Structure
📂 Project Root
```
│── Home.py
│── helpers.py
│── main.py
│── requirements.txt
│── README.md
│
├── 📁 _pages/
│ ├── _1_Food_Logging.py
│ ├── _2_AI_Suggestions.py
│ └── _3_Visualization.py
│
├── 📁 data/
│ ├── meals.csv
│ └── <username>_meals.csv
```

- Each module handles a **single responsibility**  
- Easy to extend with new features (progress reports, APIs, goals, etc.)

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| **Frontend/UI** | Streamlit, Python, Session State |
| **Backend Logic** | Python, OpenAI API |
| **Data Storage** | CSV (User-specific), Pandas, USDA dataset |
| **AI Recommendation Engine** | Rule-based + NLP model, OpenAI API |
| **Libraries** | Pandas, Streamlit, Numpy |
| **Graphs** | Matplotlib, Streamlit Charts |
---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/srivallinalla12/calories-nutrition-tracker-app.git
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run main.py
```

---


## 🧪 How It Works Internally

### Session State
- Stores logged-in user  
- Tracks meals for selected dates  
- Handles edit mode & page state  

### CSV Storage
- User data saved in real-time  
- Auto-creates new user meal files  
- Ensures persistent logs across sessions  

### AI System
The AI uses:
- Calorie target  
- Goal type  
- Veg / Non-veg preference  

to output structured meal recommendations.

#### Example Logic:
```python
if goal == "weight_loss":
    recommend(high_protein, low_calorie)
elif goal == "weight_gain":
    recommend(calorie_dense, healthy_fats)
else:
    recommend(balanced_macros)
```

---

## 🌟 Why This Project Stands Out

✔ Authentication + session management  
✔ Persistent storage without a database  
✔ Clean, scalable architecture  
✔ AI-powered nutrition suggestions  
✔ Professional Streamlit UI  
✔ Perfect as a real portfolio project showcasing:

- Backend logic  
- Data engineering  
- AI design  
- UI/UX  
- State management  
- File-based architecture  

---

## 📌 Future Enhancements

- Google Fit / Fitbit API integration  
- MongoDB / PostgreSQL database support  
- Progress dashboard with goals  
- Weekly reports  
- Food barcode scanning  
- Mobile-responsive UI  

---

## 👩‍💻 Authors

**Srivalli Nalla**  
**Gyanu Basnet**  
**Sulav Bista**

---
