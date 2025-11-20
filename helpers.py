import json
import os
from datetime import date

LOG_FILE = "data/daily_logs.json"   # saved inside data/ folder

def load_logs():
    """Load the daily logs JSON from the data folder."""
    if not os.path.exists(LOG_FILE):
        return {}

    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_logs(logs):
    """Save logs to the data folder."""
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def load_today_logs():
    """Load today's logs or create an empty entry."""
    logs = load_logs()
    today_str = str(date.today())

    if today_str not in logs:
        logs[today_str] = []

    return logs, today_str

