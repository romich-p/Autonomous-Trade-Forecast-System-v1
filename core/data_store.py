# core/data_store.py
import datetime
from tinydb import TinyDB, Query
import os

# Исключённые таймфреймы
EXCLUDED_TIMEFRAMES = {"5S", "45S", "10M"}

# Пути к БД
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
db = TinyDB(DB_PATH)

def store_candle(data):
    if data["timeframe"] in EXCLUDED_TIMEFRAMES:
        return

    key = f"{data['ticker']}_{data['timeframe']}"
    table = db.table("candles")

    # Проверка на дубликат
    Candle = Query()
    exists = table.get((Candle.key == key) & (Candle.time == data["time"]))
    if exists:
        return

    item = {
        "key": key,
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }
    table.insert(item)

def store_signal(data, advanced=False):
    if data["timeframe"] in EXCLUDED_TIMEFRAMES:
        return

    table = db.table("advanced_signals" if advanced else "signals")
    entry = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data.get("time", datetime.datetime.utcnow().isoformat()),
        "action": data["action"]
    }

    if advanced:
        entry["side"] = data.get("side", "flat")
        entry["sltp"] = float(data.get("sltp", 0))
    else:
        entry["contracts"] = float(data.get("contracts", 0))
        entry["position_size"] = float(data.get("position_size", 0))

    table.insert(entry)

def load_all():
    candles = {}
    for row in db.table("candles").all():
        key = row["key"]
        if key not in candles:
            candles[key] = []
        candles[key].append(row)

    signals = {}
    for row in db.table("signals").all():
        key = f"{row['ticker']}_{row['timeframe']}"
        if key not in signals:
            signals[key] = []
        signals[key].append(row)

    advanced_signals = {}
    for row in db.table("advanced_signals").all():
        key = f"{row['ticker']}_{row['timeframe']}"
        if key not in advanced_signals:
            advanced_signals[key] = []
        advanced_signals[key].append(row)

    return candles, signals, advanced_signals
