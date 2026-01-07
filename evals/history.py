import json
import os

HISTORY_FILE = "evals/history/results.json"
BASELINE_FILE = "evals/history/baseline.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {"runs": []}

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrupted or partial file — start fresh
        return {"runs": []}


def save_result(result: dict):
    history = load_history()
    history["runs"].append(result)

    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def save_baseline(result: dict):
    os.makedirs(os.path.dirname(BASELINE_FILE), exist_ok=True)
    with open(BASELINE_FILE, "w") as f:
        json.dump(result, f, indent=2)


def load_baseline(path: str):
    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)

