import os
import json
from pathlib import Path
from tinydb import TinyDB, Query

# Новый путь к базе данных — на постоянном хранилище Render
DB_PATH = Path("/persistent/db.json")
os.makedirs(DB_PATH.parent, exist_ok=True)
db = TinyDB(DB_PATH)

# Таблицы
candles_table = db.table("candles")
signals_table = db.table("signals")
adv_table = db.table("advanced")

# В памяти (кеш)
candles = {}           # { "GBPUSD_15S": [...] }
signals = {}           # { ("GBPUSD", "15S"): [...] }
advanced_signals = {}  # { ("GBPUSD", "15S"): [...] }

def load_data():
    global candles, signals, advanced_signals

    candles = {}
    for entry in candles_table.all():
        key = entry["key"]
        if key not in candles:
            candles[key] = []
        candles[key].append(entry["data"])

    signals = {}
    for entry in signals_table.all():
        key = tuple(entry["key"])
        if key not in signals:
            signals[key] = []
        signals[key].append(entry["data"])

    advanced_signals = {}
    for entry in adv_table.all():
        key = tuple(entry["key"])
        if key not in advanced_signals:
            advanced_signals[key] = []
        advanced_signals[key].append(entry["data"])

    print(f"[DB] Загружено: {sum(len(v) for v in candles.values())} свечей, "
          f"{sum(len(v) for v in signals.values())} сигналов, "
          f"{sum(len(v) for v in advanced_signals.values())} advanced")

def store_candle(ticker: str, timeframe: str, candle: dict):
    key = f"{ticker}_{timeframe}"
    candles.setdefault(key, []).append(candle)
    candles_table.insert({"key": key, "data": candle})

def store_signal(ticker: str, timeframe: str, signal: dict):
    key = (ticker, timeframe)
    signals.setdefault(key, []).append(signal)
    signals_table.insert({"key": list(key), "data": signal})

def store_advanced(ticker: str, timeframe: str, signal: dict):
    key = (ticker, timeframe)
    advanced_signals.setdefault(key, []).append(signal)
    adv_table.insert({"key": list(key), "data": signal})

# Инициализация при старте
load_data()
