import os
import datetime
from tinydb import TinyDB, Query

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
db = TinyDB(DB_PATH)

# === Хранилища в памяти ===
candles = {}  # (ticker, timeframe) -> [candles]
signals = {}  # (ticker, timeframe) -> [signals]
advanced_signals = {}  # (ticker, timeframe) -> [adv_signals]

# === Инициализация: загружаем из базы ===
def load_all():
    for item in db.table("candles").all():
        key = (item["ticker"], item["timeframe"])
        candles.setdefault(key, []).append(item)

    for item in db.table("signals").all():
        key = (item["ticker"], item["timeframe"])
        signals.setdefault(key, []).append(item)

    for item in db.table("advanced_signals").all():
        key = (item["ticker"], item["timeframe"])
        advanced_signals.setdefault(key, []).append(item)

load_all()

# === Сохранение свечи ===
def store_candle(data):
    key = (data["ticker"], data["timeframe"])
    if key not in candles:
        candles[key] = []

    if any(c["time"] == data["time"] for c in candles[key]):
        return

    entry = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }
    candles[key].append(entry)
    candles[key].sort(key=lambda x: x["time"])
    db.table("candles").insert(entry)

# === Получить последние свечи ===
def get_recent_candles(key, n=100):
    return candles.get(key, [])[-n:]

# === Сохранение сигналов ===
def store_signal(data, advanced=False):
    key = (data["ticker"], data["timeframe"])
    now_time = data.get("time", datetime.datetime.utcnow().isoformat())

    if advanced:
        entry = {
            "ticker": data["ticker"],
            "timeframe": data["timeframe"],
            "time": now_time,
            "action": data["action"],
            "sltp": float(data.get("sltp", 0)),
            "side": data.get("side", "flat")
        }
        advanced_signals.setdefault(key, []).append(entry)
        db.table("advanced_signals").insert(entry)
    else:
        entry = {
            "ticker": data["ticker"],
            "timeframe": data["timeframe"],
            "time": now_time,
            "action": data["action"],
            "contracts": float(data.get("contracts", 0)),
            "position_size": float(data.get("position_size", 0))
        }
        signals.setdefault(key, []).append(entry)
        db.table("signals").insert(entry)
