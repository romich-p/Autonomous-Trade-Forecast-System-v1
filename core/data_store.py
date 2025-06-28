import os
import json

DB_PATH = os.environ.get("DB_PATH", "db.json")

# Создаём директорию, если указана
if os.path.dirname(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def load_database():
    if not os.path.exists(DB_PATH):
        print("[DB] db.json не найден, создаём новый файл")
        return {}
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[DB] Ошибка загрузки базы: {e}")
        return {}

def save_database(db):
    try:
        with open(DB_PATH, "w") as f:
            json.dump(db, f)
    except Exception as e:
        print(f"[DB] Ошибка сохранения базы: {e}")

def get_candles(ticker, timeframe):
    db = load_database()
    key = f"{ticker}_{timeframe}"
    return db.get(key, {}).get("candles", [])

def get_signals(ticker, timeframe):
    db = load_database()
    key = f"{ticker}_{timeframe}"
    return db.get(key, {}).get("signals", [])

def get_advanced_signals(ticker, timeframe):
    db = load_database()
    key = f"{ticker}_{timeframe}"
    return db.get(key, {}).get("advanced", [])
