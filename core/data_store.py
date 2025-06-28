import os
import json
from tinydb import TinyDB, Query

DB_PATH = "db.json"

# Гарантируем, что директория под файл существует
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

# Загружаем TinyDB
db = TinyDB(DB_PATH)

# Режим отладки
DEBUG = True

def log(*args):
    if DEBUG:
        print("[DB]", *args)

# --- LOW LEVEL ---

def load_database():
    try:
        with open(DB_PATH, "r") as f:
            data = json.load(f)
            log("Загружена база:", list(data.keys()))
            return data
    except Exception as e:
        log("Ошибка загрузки базы:", e)
        return {
            "candles": {},
            "signals": {},
            "advanced_signals": {}
        }

def save_database(data):
    try:
        with open(DB_PATH, "w") as f:
            json.dump(data, f, indent=2)
        log("База сохранена.")
    except Exception as e:
        log("Ошибка сохранения базы:", e)

# --- HIGH LEVEL ---

def store_candle(payload):
    data = load_database()
    key = f"{payload['ticker']}_{payload['timeframe']}"
    record = {
        "time": payload["time"],
        "open": payload["open"],
        "high": payload["high"],
        "low": payload["low"],
        "close": payload["close"],
        "volume": payload["volume"]
    }
    data.setdefault("candles", {}).setdefault(key, []).append(record)
    log(f"Добавлена свеча {key} ->", record)
    save_database(data)

def store_signal(payload):
    data = load_database()
    key = f"{payload['ticker']}_{payload['timeframe']}"
    signal = {
        "time": payload["time"],
        "strategy": payload.get("strategy"),
        "signal": payload.get("signal"),
        "side": payload.get("side")
    }
    data.setdefault("signals", {}).setdefault(key, []).append(signal)
    log(f"Добавлен сигнал {key} ->", signal)
    save_database(data)

def store_advanced(payload):
    data = load_database()
    key = f"{payload['ticker']}_{payload['timeframe']}"
    result = {
        "time": payload["time"],
        "trend": payload.get("trend"),
        "entry_score": payload.get("entry_score"),
        "side": payload.get("side")
    }
    data.setdefault("advanced_signals", {}).setdefault(key, []).append(result)
    log(f"Добавлен advanced сигнал {key} ->", result)
    save_database(data)

# --- READERS ---

def get_candles(ticker, timeframe):
    data = load_database()
    key = f"{ticker}_{timeframe}"
    return data.get("candles", {}).get(key, [])

def get_signals(ticker, timeframe):
    data = load_database()
    key = f"{ticker}_{timeframe}"
    return data.get("signals", {}).get(key, [])

def get_advanced_signals(ticker, timeframe):
    data = load_database()
    key = f"{ticker}_{timeframe}"
    return data.get("advanced_signals", {}).get(key, [])
