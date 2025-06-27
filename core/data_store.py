import os
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

db = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage))
candles_table = db.table("candles")
signals_table = db.table("signals")
adv_signals_table = db.table("advanced_signals")

candles = {}
signals = {}
advanced_signals = {}

def load_all():
    global candles, signals, advanced_signals

    candles.clear()
    signals.clear()
    advanced_signals.clear()

    for row in candles_table.all():
        key = (row["ticker"], row["timeframe"])
        candles.setdefault(key, []).append(row["data"])

    for row in signals_table.all():
        key = (row["ticker"], row["timeframe"])
        signals.setdefault(key, []).append(row["data"])

    for row in adv_signals_table.all():
        key = (row["ticker"], row["timeframe"])
        advanced_signals.setdefault(key, []).append(row["data"])

load_all()

def store_candle(data):
    key = (data["ticker"], data["timeframe"])
    if key not in candles:
        candles[key] = []

    if any(c["time"] == data["time"] for c in candles[key]):
        return

    entry = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0)),
    }

    candles[key].append(entry)
    candles[key].sort(key=lambda x: x["time"])
    candles_table.insert({"ticker": data["ticker"], "timeframe": data["timeframe"], "data": entry})

def store_signal(data, advanced=False):
    key = (data["ticker"], data["timeframe"])
    target = advanced_signals if advanced else signals
    table = adv_signals_table if advanced else signals_table

    entry = {
        "time": data["time"],
        "action": data["action"]
    }

    if advanced:
        entry["sltp"] = float(data.get("sltp", 0))
        entry["side"] = data.get("side", "flat")
    else:
        entry["contracts"] = float(data.get("contracts", 0))
        entry["position_size"] = float(data.get("position_size", 0))

    target.setdefault(key, []).append(entry)
    table.insert({"ticker": data["ticker"], "timeframe": data["timeframe"], "data": entry})
