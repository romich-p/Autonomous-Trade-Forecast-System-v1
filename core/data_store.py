import os
import json
from tinydb import TinyDB, Query
from collections import defaultdict

DB_PATH = "db.json"
db = TinyDB(DB_PATH)

# Хранилища в памяти
candles = defaultdict(list)
signals = defaultdict(list)
advanced_signals = defaultdict(list)

def load_data():
    if not os.path.exists(DB_PATH):
        print("[DB] db.json не найден, создаём новый файл")
        return candles, signals, advanced_signals

    print("[DB] Загружаем данные из db.json...")
    for row in db.all():
        dtype = row.get("type")
        key = (row["ticker"], row["timeframe"])
        if dtype == "candle":
            candles[key].append(row["candle"])
        elif dtype == "signal":
            signals[key].append(row["signal"])
        elif dtype == "advanced":
            advanced_signals[key].append(row["advanced"])
    print(f"[DB] Загружено: {sum(map(len, candles.values()))} свечей, {sum(map(len, signals.values()))} сигналов, {sum(map(len, advanced_signals.values()))} advanced")
    return candles, signals, advanced_signals

def store_candle(ticker, timeframe, candle):
    key = (ticker, timeframe)
    candles[key].append(candle)
    db.insert({"type": "candle", "ticker": ticker, "timeframe": timeframe, "candle": candle})

def store_signal(ticker, timeframe, signal):
    key = (ticker, timeframe)
    signals[key].append(signal)
    db.insert({"type": "signal", "ticker": ticker, "timeframe": timeframe, "signal": signal})

def store_advanced(ticker, timeframe, advanced):
    key = (ticker, timeframe)
    advanced_signals[key].append(advanced)
    db.insert({"type": "advanced", "ticker": ticker, "timeframe": timeframe, "advanced": advanced})
