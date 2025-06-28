import os
import json
from tinydb import TinyDB, Query

DB_PATH = "db.json"

# Гарантируем, что папка существует
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

# Загрузка всей базы
def load_database():
    if not os.path.exists(DB_PATH):
        print("[DB] db.json не найден, создаём новый файл")
        save_database({})
        return {}
    with open(DB_PATH, "r") as f:
        return json.load(f)

# Сохранение всей базы
def save_database(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f)

# Прочие функции, например:
def store_candle(ticker, timeframe, candle):
    db = load_database()
    key = f"{ticker}_{timeframe}"
    db.setdefault(key, {}).setdefault("candles", []).append(candle)
    save_database(db)

def get_candles(ticker, timeframe):
    db = load_database()
    return db.get(f"{ticker}_{timeframe}", {}).get("candles", [])

def get_signals(ticker, timeframe):
    db = load_database()
    return db.get(f"{ticker}_{timeframe}", {}).get("signals", [])

def get_advanced_signals(ticker, timeframe):
    db = load_database()
    return db.get(f"{ticker}_{timeframe}", {}).get("advanced", [])

def store_signal(ticker, timeframe, signal):
    db = load_database()
    key = f"{ticker}_{timeframe}"
    db.setdefault(key, {}).setdefault("signals", []).append(signal)
    save_database(db)

def store_advanced(ticker, timeframe, signal):
    db = load_database()
    key = f"{ticker}_{timeframe}"
    db.setdefault(key, {}).setdefault("advanced", []).append(signal)
    save_database(db)
