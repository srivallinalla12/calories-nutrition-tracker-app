# AI-Powered Calorie & Nutrition Tracker  
*A simple student project created using Streamlit, Python, OpenAI API and basic data processing tools.
---
## Overview
This project lets users track their daily meals, monitor calories, and visualize macronutrients.  
It also provides basic AI-generated suggestions personalized for each user.
---
## Project Structure
.
├── Home.py
├── main.py
├── helpers.py
├── requirements.txt
├── USDA.csv
├── healthy_meals.csv
├── _pages/
│ ├── _1_Food_Logging.py
│ ├── _2_AI_Suggestions.py
│ ├── 3_Visualization.py
├── data/
│ ├── users.json
│ ├── meals.csv, sulav_meals.csv, daily_logs*.json
│ ├── goal files
└── README.md
---
## Login System
- Simple file-based login
- Usernames are stored in `data/users.json`  
- Each user gets their own meal history file  
- Demo user is included for quick testing
---
## Meal Logging
Users can:
- Log foods from:
  - USDA Dataset
  - Manual Entry
- Track:
  - Calories  
  - Protein  
  - Carbs  
  - Fat  
- All logs saved in `data/{username}_meals.csv`

---

## AI Meal Suggestions
The app uses **OpenAI API** for:
- Healthy meal ideas  
- Feedback based on the user's personal needs
- Simple goal-based suggestions  

This is **not a machine learning model**.  
It is just making API calls to OpenAI.
---

## Visualizations
Users can get visual insights of:
- Daily macro breakdown  
- Calories over time  
- Pie charts for macros & calories  
- Stacked bar charts  
- Cumulative macro timeline  
- Horizontal macro proportion chart  

Charts use **Matplotlib**.
---

## How It Works
- Users log meals  
- Data is stored in CSV files  
- Streamlit pages read and visualize the data  
- AI suggestions are generated via API  
---

## Installation

### 1. Clone the project
git clone https://github.com/srivallinalla12/calories-nutrition-tracker-app.git 
cd calories-nutrition-tracker-app


### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your OpenAI API key
To get AI-powered suggestions, create a `.env` file and add your key:

OPENAI_API_KEY=your_api_key

Note: If you don’t add a key, the app will still work for meal logging and visualization. Only the AI suggestions will be disabled. The OpenAI API key is not included here for security reasons. You’ll need to add your own key to use the AI features.

### 4. Run the app
streamlit run main.py
---

## Demo User
You can log in as:
username: demo
password: demo123

This user loads sample data for quick testing.
---

## Features (Summary)
- Simple login  
- Meal logging  
- AI suggestions  
- Daily calorie and macro visualization  
- Week/Month/Year calorie graphs  

---

## Contributors
- **Gyanu Basnet**
- **Sulav Bista**
- **Srivalli Nalla** 

---

## Notes
This project is designed for learning and presentation purposes.  
It is **not** intended for medical/health professional use.
---

## License
MIT License


