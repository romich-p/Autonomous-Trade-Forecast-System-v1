import os
import json
from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

DB_PATH = os.getenv("DB_PATH", "db.json")

# Гарантируем, что директория существует
if os.path.dirname(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

db = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage))

# Внутренняя структура
candles = {}  # {ticker: {timeframe: [candles]}}
signals = {}  # {ticker: {timeframe: [signals]}}
advanced_signals = {}  # {ticker: {timeframe: [advanced]}}

def normalize_ticker(ticker: str) -> str:
    return ticker.upper()

def store_candle(data):
    ticker = normalize_ticker(data["ticker"])
    timeframe = data["timeframe"]

    candles.setdefault(ticker, {}).setdefault(timeframe, []).append(data)
    db.table("candles").insert(data)

    print(f"[STORE] candle: {ticker} {timeframe} {data['time']}")

def store_signal(data):
    ticker = normalize_ticker(data["ticker"])
    timeframe = data["timeframe"]

    signals.setdefault(ticker, {}).setdefault(timeframe, []).append(data)
    db.table("signals").insert(data)

    print(f"[STORE] signal: {ticker} {timeframe} {data.get('side', '?')}")

def store_advanced(data):
    ticker = normalize_ticker(data["ticker"])
    timeframe = data["timeframe"]

    advanced_signals.setdefault(ticker, {}).setdefault(timeframe, []).append(data)
    db.table("advanced").insert(data)

    print(f"[STORE] advanced: {ticker} {timeframe} {data.get('trend_probability', '?')}")

def get_candles(ticker, timeframe):
    return candles.get(normalize_ticker(ticker), {}).get(timeframe, [])

def get_signals(ticker, timeframe):
    return signals.get(normalize_ticker(ticker), {}).get(timeframe, [])

def get_advanced_signals(ticker, timeframe):
    return advanced_signals.get(normalize_ticker(ticker), {}).get(timeframe, [])

def get_all_pairs():
    return list(candles.keys())

def load_database():
    for row in db.table("candles"):
        store_candle(row)

    for row in db.table("signals"):
        store_signal(row)

    for row in db.table("advanced"):
        store_advanced(row)

    print(f"[DB] Загружено: {sum(len(t) for t in candles.values())} свечей, "
          f"{sum(len(t) for t in signals.values())} сигналов, "
          f"{sum(len(t) for t in advanced_signals.values())} advanced")
