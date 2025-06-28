import json
import os
from typing import Optional

DB_PATH = "db.json"

DEFAULT_DB_STRUCTURE = {
    "candles": {},
    "signals": {},
    "advanced_signals": {}
}

# Инициализация базы при старте
if not os.path.exists(DB_PATH) or os.stat(DB_PATH).st_size == 0:
    with open(DB_PATH, "w") as f:
        json.dump(DEFAULT_DB_STRUCTURE, f)


def load_database() -> dict:
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[DB] Ошибка загрузки базы: {e}")
        return DEFAULT_DB_STRUCTURE.copy()


def save_database(db: dict):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)


def store_candle(ticker: str, timeframe: str, candle: dict):
    db = load_database()
    candles = db.setdefault("candles", {})
    key = f"{ticker}|{timeframe}"
    candles.setdefault(key, []).append(candle)
    save_database(db)


def store_signal(ticker: str, timeframe: str, signal: dict):
    db = load_database()
    signals = db.setdefault("signals", {})
    key = f"{ticker}|{timeframe}"
    signals.setdefault(key, []).append(signal)
    save_database(db)


def store_advanced(ticker: str, timeframe: str, signal: dict):
    db = load_database()
    signals = db.setdefault("advanced_signals", {})
    key = f"{ticker}|{timeframe}"
    signals.setdefault(key, []).append(signal)
    save_database(db)


def get_candles(ticker: str, timeframe: str) -> list:
    db = load_database()
    return db.get("candles", {}).get(f"{ticker}|{timeframe}", [])


def get_signals(ticker: str, timeframe: str) -> list:
    db = load_database()
    return db.get("signals", {}).get(f"{ticker}|{timeframe}", [])


def get_advanced_signals(ticker: str, timeframe: str) -> list:
    db = load_database()
    return db.get("advanced_signals", {}).get(f"{ticker}|{timeframe}", [])
