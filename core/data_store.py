import os
import json
from collections import defaultdict

DB_PATH = "db.json"

# Создаём пустую структуру, если файл отсутствует
if not os.path.exists(DB_PATH):
    print("[DB] db.json не найден, создаём новый файл")
    with open(DB_PATH, "w") as f:
        json.dump({}, f)

def load_database():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_database(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

def store_candle(ticker, timeframe, data):
    db = load_database()
    key = f"{ticker}:{timeframe}"
    db.setdefault(key, {}).setdefault("candles", []).append(data)
    save_database(db)

def store_signal(ticker, timeframe, data):
    db = load_database()
    key = f"{ticker}:{timeframe}"
    db.setdefault(key, {}).setdefault("signals", []).append(data)
    save_database(db)

def store_advanced(ticker, timeframe, data):
    db = load_database()
    key = f"{ticker}:{timeframe}"
    db.setdefault(key, {}).setdefault("advanced_signals", []).append(data)
    save_database(db)

def get_candles(ticker, timeframe):
    db = load_database()
    return db.get(f"{ticker}:{timeframe}", {}).get("candles", [])

def get_signals(ticker, timeframe):
    db = load_database()
    return db.get(f"{ticker}:{timeframe}", {}).get("signals", [])

def get_advanced_signals(ticker, timeframe):
    db = load_database()
    return db.get(f"{ticker}:{timeframe}", {}).get("advanced_signals", [])
