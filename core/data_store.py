import os
import json
from tinydb import TinyDB, Query

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "db.json")
db = TinyDB(DB_PATH)

# Кэш в памяти
candles = {}
signals = {}
advanced_signals = {}

def load_database():
    global candles, signals, advanced_signals
    try:
        candles = db.table("candles").all()[0] if db.table("candles").all() else {}
        signals = db.table("signals").all()[0] if db.table("signals").all() else {}
        advanced_signals = db.table("advanced_signals").all()[0] if db.table("advanced_signals").all() else {}
        print(f"[DB] Загружено: {len(candles)} свечей, {len(signals)} сигналов, {len(advanced_signals)} advanced")
    except Exception as e:
        print("[DB] Ошибка загрузки:", e)

def save_database():
    db.table("candles").truncate()
    db.table("candles").insert(candles)
    db.table("signals").truncate()
    db.table("signals").insert(signals)
    db.table("advanced_signals").truncate()
    db.table("advanced_signals").insert(advanced_signals)

def store_candle(ticker: str, timeframe: str, candle: dict):
    key = f"{ticker}_{timeframe}"
    candles.setdefault(key, []).append(candle)
    candles[key] = sorted({c["time"]: c for c in candles[key]}.values(), key=lambda x: x["time"])
    save_database()

def store_signal(ticker: str, timeframe: str, signal: dict):
    key = (ticker, timeframe)
    signals.setdefault(key, []).append(signal)
    save_database()

def store_advanced(ticker: str, timeframe: str, advanced: dict):
    key = (ticker, timeframe)
    advanced_signals.setdefault(key, []).append(advanced)
    save_database()
