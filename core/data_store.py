import os
import json
from tinydb import TinyDB, Query
from collections import defaultdict

DB_PATH = "db.json"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

if not os.path.exists(DB_PATH):
    print("[DB] db.json не найден, создаём новый файл")
    with open(DB_PATH, "w") as f:
        json.dump({}, f)

db = TinyDB(DB_PATH)
candles = defaultdict(lambda: defaultdict(list))
signals = defaultdict(lambda: defaultdict(list))
advanced_signals = defaultdict(lambda: defaultdict(list))


def load_all_data():
    global candles, signals, advanced_signals
    candles = defaultdict(lambda: defaultdict(list))
    signals = defaultdict(lambda: defaultdict(list))
    advanced_signals = defaultdict(lambda: defaultdict(list))
    for row in db.all():
        t = row.get("type")
        ticker = row.get("ticker")
        tf = row.get("timeframe")
        if t == "candle":
            candles[ticker][tf].append(row["data"])
        elif t == "signal":
            signals[ticker][tf].append(row["data"])
        elif t == "advanced":
            advanced_signals[ticker][tf].append(row["data"])
    print(f"[DB] Загружено: {sum(len(v) for tf in candles.values() for v in tf.values())} свечей, "
          f"{sum(len(v) for tf in signals.values() for v in tf.values())} сигналов, "
          f"{sum(len(v) for tf in advanced_signals.values() for v in tf.values())} advanced")


def store_candle(ticker, timeframe, candle):
    db.insert({
        "type": "candle",
        "ticker": ticker,
        "timeframe": timeframe,
        "data": candle
    })
    candles[ticker][timeframe].append(candle)


def store_signal(ticker, timeframe, signal):
    db.insert({
        "type": "signal",
        "ticker": ticker,
        "timeframe": timeframe,
        "data": signal
    })
    signals[ticker][timeframe].append(signal)


def store_advanced(ticker, timeframe, advanced_signal):
    db.insert({
        "type": "advanced",
        "ticker": ticker,
        "timeframe": timeframe,
        "data": advanced_signal
    })
    advanced_signals[ticker][timeframe].append(advanced_signal)


def get_candles(ticker, timeframe):
    return candles.get(ticker, {}).get(timeframe, [])


def get_signals(ticker, timeframe):
    return signals.get(ticker, {}).get(timeframe, [])


def get_advanced_signals(ticker, timeframe):
    return advanced_signals.get(ticker, {}).get(timeframe, [])
