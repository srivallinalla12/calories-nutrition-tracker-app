# main.py
import streamlit as st
import os
import json
from datetime import datetime
from _pages import _1_Food_Logging, _2_AI_Suggestions, _3_Visualization
from Home import home_page

# ---------------------------
# Data paths
# ---------------------------
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")

os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)


# --------------------------------
# USER-SPECIFIC DATA INITIALIZATION
# --------------------------------
def initialize_user_files(username):
    """
    Creates user-specific daily log file ONLY for new users.
    Demo user keeps demo file and is never overwritten.
    """
    if username.lower() == "demo":
        demo_file = "data/daily_logs_demo.json"
        if not os.path.exists(demo_file):
            with open(demo_file, "w") as f:
                json.dump({}, f)
        return

    user_file = f"data/daily_logs_{username}.json"

    # Create a fresh empty log file for new users only
    if not os.path.exists(user_file):
        with open(user_file, "w") as f:
            json.dump({}, f)


# ---------------------------
# Session State Defaults
# ---------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "Welcome"


# ---------------------------
# Helper functions
# ---------------------------
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def login_user(username, password):
    users = load_users()

    for u in users:
        if u["username"] == username and u["password"] == password:
            st.session_state["user"] = username
            st.session_state["page"] = "Home"

            # Initialize correct log file for this user
            initialize_user_files(username)

            # Trigger rerun safely
            st.session_state["login_trigger"] = not st.session_state.get("login_trigger", False)
            return True

    st.error("Invalid username or password")
    return False


def signup_user(username, password):
    users = load_users()

    if any(u["username"] == username for u in users):
        st.error("Username already exists")
        return False

    users.append({"username": username, "password": password})
    save_users(users)

    # Create fresh empty log file for new user
    initialize_user_files(username)

    st.success("Sign up successful! Please log in.")
    return True


# ---------------------------
# Quick Navigation Handler
# ---------------------------
if "nav_to" in st.session_state:
    st.session_state["page"] = st.session_state.pop("nav_to")


# ---------------------------
# Show appropriate page
# ---------------------------
if st.session_state["user"] is None:

    # ---------------------------
    # Welcome / Login / Signup
    # ---------------------------
    st.set_page_config(page_title="Calorie & Nutrition Tracker", layout="wide")
    st.title("🍎 Calorie & Nutrition Tracker")
    st.write("Please log in or sign up to continue.")
    st.info("Double click the Login button if it doesn't work first time.")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            login_user(username, password)

    with tab2:
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")

        if st.button("Sign Up"):
            signup_user(new_user, new_pass)

else:
    # ---------------------------
    # Main App with Sidebar
    # ---------------------------
    st.set_page_config(page_title="Calorie & Nutrition Tracker", layout="wide")

    st.sidebar.title(f"Welcome, {st.session_state['user']} ✅")

    available_pages = ["Home", "Food Logging", "AI Suggestions", "Visualization"]

    page = st.sidebar.radio(
        "Navigate",
        available_pages,
        index=available_pages.index(st.session_state["page"])
        if st.session_state["page"] in available_pages else 0
    )

    # Logout
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"user": None, "page": "Welcome"}))

    # Update current page
    st.session_state["page"] = page

    # ---------------------------
    # Render selected page
    # ---------------------------
    if page == "Home":
        home_page()
    elif page == "Food Logging":
        _1_Food_Logging.food_logging_page()
    elif page == "AI Suggestions":
        _2_AI_Suggestions.ai_suggestions_page()
    elif page == "Visualization":
        _3_Visualization.visualization_page()
