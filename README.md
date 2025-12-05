⭐ Nutrition & Calorie Tracking App (Streamlit)
A personalized nutrition-tracking web application built with Python, Streamlit, and Pandas, featuring AI-powered meal suggestions, daily food logging, macro visualization, and user-specific data storage.
Designed to help users track calories, improve diet habits, and receive targeted meal recommendations for weight loss, maintenance, or muscle gain.
🚀 Features
🔐 1. Secure Login & Session Management
Each user gets a unique session using st.session_state["user"].
Personalized meal logs are stored under the user’s own CSV file:
data/<username>_meals.csv
Demo user support included.
🍽️ 2. Meal Logging System
Users can log meals with the following details:
Calories
Protein
Carbs
Fat
Date
Real-time updates using st.rerun() for:
Adding meals
Editing meals
Deleting meals
Data stored dynamically in both:
Session state
User-specific CSV
🤖 3. AI Meal Recommendations
Smart meal suggestions powered by an AI model built around:
Target calorie input
User goal (Weight Loss / Maintenance / Weight Gain)
Vegetarian / Non-Veg preference
The AI provides balanced meal ideas based on:
Calorie density
Macro structure
Weight-management strategy
Examples:
Weight Loss → high-protein, low-calorie meals
Weight Gain → high-calorie, nutrient-dense meals
Balanced → controlled macros matched to calorie target
📊 4. Interactive Nutrition Visualization
Users can view trends over time:
Total Calories
Protein Intake
Carbs
Fat
Includes:
Daily aggregation
Clean data validation
Dynamic Streamlit charts
This helps users understand dietary patterns and adjust accordingly.
🧱 5. Modular Application Architecture
Clean project layout for scalability:
📂 Project Root
│── Home.py
│── helpers.py
│── main.py
│── requirements.txt
│── README.md
│
├── 📁 _pages/
│     ├── _1_Food_Logging.py
│     ├── _2_AI_Suggestions.py
│     └── _3_Visualization.py
│
├── 📁 data/
│     ├── meals.csv
│     └── <username>_meals.csv
│

Each module handles a single responsibility
Easy to extend with new features (e.g., progress reports, goals, APIs)
🛠️ Tech Stack
Component	Technology
Frontend/UI	Streamlit
Backend Logic	Python
Data Storage	CSV (User-specific)
AI Recommendation Engine	Rule-based + NLP model
Libraries	Pandas, Streamlit, Numpy
⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
2. Install Dependencies
pip install -r requirements.txt
3. Run the App
streamlit run main.py
🧪 How It Works Internally
Session State
Stores logged-in user
Tracks all meals for selected dates
Stores edit modes & UI state
CSV Storage
App writes and reads user data in real time
Auto-creates files for new users
Ensures persistent logs between sessions
AI System
The AI uses:
Calorie target
Goal type
Meal preference
to generate structured nutritional recommendations.
Example internal logic:
if goal == "weight_loss":
    recommend(high_protein, low_calorie)
elif goal == "weight_gain":
    recommend(calorie_dense, healthy_fats)
else:
    recommend(balanced_macros)
🌟 Why This Project Stands Out
✔ Full authentication + session management
✔ Persistent storage without a database
✔ Clean, modular structure ready for scale
✔ AI-powered nutrition suggestions
✔ Professional-grade UI/UX using Streamlit
✔ Well-structured code suitable for real-world deployment
Designed as a portfolio-quality project to showcase skills in:
Backend Development
Data Engineering
AI Logic Design
UI/UX with Streamlit
State Management
File-Based Data Architecture
📌 Future Enhancements
Integration with Fitness APIs (e.g., Fitbit, Google Fit)
Cloud database (MongoDB or PostgreSQL)
User goals dashboard
Weekly progress reports
Barcode scanning for food items
Mobile-optimized layout
👩‍💻 Author
Srivalli Nalla
Gyanu Basnet
Sulav Bista
