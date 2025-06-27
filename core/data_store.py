import os
import datetime
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
db = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage))

# ==== Оперативное хранилище ====
candles = {}  # {(ticker, timeframe): [candles]}
signals = {}  # {(ticker, timeframe): [signals]}
advanced_signals = {}  # {(ticker, timeframe): [advanced_signals]}

# ==== Загрузка из БД ====
def load_data():
    global candles, signals, advanced_signals
    candles_table = db.table("candles")
    signals_table = db.table("signals")
    advanced_table = db.table("advanced_signals")

    for item in candles_table.all():
        key = (item["ticker"], item["timeframe"])
        candles.setdefault(key, []).append(item)

    for item in signals_table.all():
        key = (item["ticker"], item["timeframe"])
        signals.setdefault(key, []).append(item)

    for item in advanced_table.all():
        key = (item["ticker"], item["timeframe"])
        advanced_signals.setdefault(key, []).append(item)

load_data()

# ==== Сохранение свечей ====
def store_candle(data):
    key = (data["ticker"], data["timeframe"])
    if key not in candles:
        candles[key] = []

    # Проверка на дубликат
    if any(c["time"] == data["time"] for c in candles[key]):
        return

    candle = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0)),
    }

    candles[key].append(candle)
    candles[key].sort(key=lambda x: x["time"])

    db.table("candles").insert(candle)

# ==== Сохранение сигналов ====
def store_signal(data, advanced=False):
    target = advanced_signals if advanced else signals
    table = db.table("advanced_signals" if advanced else "signals")

    key = (data["ticker"], data["timeframe"])
    target.setdefault(key, [])

    signal = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data.get("time", datetime.datetime.utcnow().isoformat()),
        "action": data["action"]
    }

    if advanced:
        signal["side"] = data.get("side", "flat")
        signal["sltp"] = float(data.get("sltp", 0))
    else:
        signal["contracts"] = float(data.get("contracts", 0))
        signal["position_size"] = float(data.get("position_size", 0))

    target[key].append(signal)
    table.insert(signal)
