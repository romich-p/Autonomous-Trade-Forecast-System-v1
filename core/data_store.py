import os
import datetime
import json
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

# Путь к файлу БД (всегда внутри /data/db.json)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "db.json")
db = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage))

# Глобальные переменные (в памяти)
candles = {}
signals = {}
advanced_signals = {}

# === Загрузка при запуске ===
def load_data_from_db():
    global candles, signals, advanced_signals

    candles.clear()
    signals.clear()
    advanced_signals.clear()

    db_data = db.all()
    for item in db_data:
        if item.get("type") == "candle":
            key = f"{item['ticker']}_{item['timeframe']}"
            candles.setdefault(key, []).append(item["data"])
        elif item.get("type") == "signal":
            key = f"{item['ticker']}_{item['timeframe']}"
            signals.setdefault(key, []).append(item["data"])
        elif item.get("type") == "signal_advanced":
            key = f"{item['ticker']}_{item['timeframe']}"
            advanced_signals.setdefault(key, []).append(item["data"])

    # Отсортировать по времени
    for dataset in [candles, signals, advanced_signals]:
        for k in dataset:
            dataset[k].sort(key=lambda x: x["time"])

    print(f"[DB] Загружено: {len(candles)} свечей, {len(signals)} сигналов, {len(advanced_signals)} advanced")

# === Сохраняем свечу ===
def store_candle(data):
    key = f"{data['ticker']}_{data['timeframe']}"
    candles.setdefault(key, [])

    if any(c['time'] == data['time'] for c in candles[key]):
        return  # дубликат

    record = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }

    candles[key].append(record)
    candles[key].sort(key=lambda x: x["time"])

    db.insert({
        "type": "candle",
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "data": record
    })

# === Сохраняем сигнал ===
def store_signal(data, advanced=False):
    key = f"{data['ticker']}_{data['timeframe']}"
    target = advanced_signals if advanced else signals
    target.setdefault(key, [])

    record = {
        "time": data.get("time", datetime.datetime.utcnow().isoformat()),
        "action": data["action"]
    }

    if advanced:
        record["side"] = data.get("side", "flat")
        record["sltp"] = float(data.get("sltp", 0))
    else:
        record["contracts"] = float(data.get("contracts", 0))
        record["position_size"] = float(data.get("position_size", 0))

    target[key].append(record)
    target[key].sort(key=lambda x: x["time"])

    db.insert({
        "type": "signal_advanced" if advanced else "signal",
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "data": record
    })


# === Вызываем при старте ===
load_data_from_db()
