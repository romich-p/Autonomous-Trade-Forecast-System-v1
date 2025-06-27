import json
import os
from collections import defaultdict
from tinydb import TinyDB

DB_PATH = "db.json"

# Используем TinyDB для сохранения
db = TinyDB(DB_PATH)

# Основные структуры для хранения данных в памяти
candles = defaultdict(list)
signals = defaultdict(list)
advanced_signals = defaultdict(list)

def load_data():
    if not os.path.exists(DB_PATH):
        print("[DB] db.json не найден, создаём новый файл")
        return

    data = db.all()
    loaded_candles = 0
    loaded_signals = 0
    loaded_advanced = 0

    for entry in data:
        if entry.get("type") == "candle":
            key = f"{entry['ticker']}_{entry['timeframe']}".upper()
            candles[key].append(entry["data"])
            loaded_candles += 1
        elif entry.get("type") == "signal":
            key = f"{entry['ticker']}_{entry['timeframe']}".upper()
            signals[key].append(entry["data"])
            loaded_signals += 1
        elif entry.get("type") == "advanced":
            key = f"{entry['ticker']}_{entry['timeframe']}".upper()
            advanced_signals[key].append(entry["data"])
            loaded_advanced += 1

    print(f"[DB] Загружено: {loaded_candles} свечей, {loaded_signals} сигналов, {loaded_advanced} advanced")

def store_candle(ticker, timeframe, candle):
    key = f"{ticker}_{timeframe}".upper()
    candles[key].append(candle)
    db.insert({
        "type": "candle",
        "ticker": ticker,
        "timeframe": timeframe,
        "data": candle
    })

def store_signal(ticker, timeframe, signal):
    key = f"{ticker}_{timeframe}".upper()
    signals[key].append(signal)
    db.insert({
        "type": "signal",
        "ticker": ticker,
        "timeframe": timeframe,
        "data": signal
    })

def store_advanced(ticker, timeframe, advanced):
    key = f"{ticker}_{timeframe}".upper()
    advanced_signals[key].append(advanced)
    db.insert({
        "type": "advanced",
        "ticker": ticker,
        "timeframe": timeframe,
        "data": advanced
    })
