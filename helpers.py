import json
import os
from datetime import date
import streamlit as st

# -------------------------------------
# Get the correct log file per user
# -------------------------------------
def get_log_file():
    username = st.session_state.get("user", None)

    if username is None:
        # User not logged in — should never happen, but safe fallback
        return "data/daily_logs_default.json"

    # Demo user → always use fixed demo file
    if username.lower() == "demo":
        return "data/daily_logs_demo.json"

    # Real user → separate file for each user
    return f"data/daily_logs_{username}.json"


# -------------------------------------
# Load logs
# -------------------------------------
def load_logs():
    LOG_FILE = get_log_file()

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(LOG_FILE):
        return {}

    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


# -------------------------------------
# Save logs
# -------------------------------------
def save_logs(logs):
    LOG_FILE = get_log_file()

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


# -------------------------------------
# Load today's logs
# -------------------------------------
def load_today_logs():
    logs = load_logs()
    today_str = str(date.today())

    # Create today's date list if missing
    if today_str not in logs:
        logs[today_str] = []

    return logs, today_str
