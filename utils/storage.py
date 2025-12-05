import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "db.json"


def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def load_db():
   
    ensure_data_dir()
    if not DATA_FILE.exists():
        return {"users": [], "projects": [], "tasks": []}

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: db.json is corrupted. Starting with empty database.")
        return {"users": [], "projects": [], "tasks": []}


def save_db(db):
    
    ensure_data_dir()
    with open(DATA_FILE, "w") as f:
        json.dump(db, f, indent=2)


def next_id(items):
   
    if not items:
        return 1
    return max(item["id"] for item in items) + 1
