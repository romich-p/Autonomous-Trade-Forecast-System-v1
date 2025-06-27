import os
import datetime
from tinydb import TinyDB, Query
from tinydb.operations import set as set_op

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
db = TinyDB(DB_PATH)

# === Хранилища в памяти ===
candles = {}  # {'GBPUSD_15S': [ {candle}, ... ]}
signals = {}
advanced_signals = {}

# === Загрузка при старте ===
def load_data():
    global candles, signals, advanced_signals

    for row in db.table("candles").all():
        key = row["key"]
        if key not in candles:
            candles[key] = []
        candles[key].append(row["data"])

    for row in db.table("signals").all():
        key = row["key"]
        if key not in signals:
            signals[key] = []
        signals[key].append(row["data"])

    for row in db.table("adv_signals").all():
        key = row["key"]
        if key not in advanced_signals:
            advanced_signals[key] = []
        advanced_signals[key].append(row["data"])

load_data()

# === Сохранение свечи ===
def store_candle(data):
    key = f"{data['ticker']}_{data['timeframe']}"
    if key not in candles:
        candles[key] = []

    if any(c['time'] == data['time'] for c in candles[key]):
        return

    candle = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }

    candles[key].append(candle)
    candles[key].sort(key=lambda x: x["time"])

    # Сохраняем в TinyDB
    db.table("candles").insert({"key": key, "data": candle})


# === Сохранение сигнала ===
def store_signal(data, advanced=False):
    table = "adv_signals" if advanced else "signals"
    target = advanced_signals if advanced else signals

    key = f"{data['ticker']}_{data['timeframe']}"
    if key not in target:
        target[key] = []

    signal_data = {
        "time": data.get("time", datetime.datetime.utcnow().isoformat()),
        "action": data["action"],
    }

    if advanced:
        signal_data["side"] = data.get("side", "flat")
        signal_data["sltp"] = float(data.get("sltp", 0))
    else:
        signal_data["contracts"] = float(data.get("contracts", 0))
        signal_data["position_size"] = float(data.get("position_size", 0))

    target[key].append(signal_data)

    # Сохраняем в TinyDB
    db.table(table).insert({"key": key, "data": signal_data})


# === Получить последние N свечей ===
def get_recent_candles(ticker_tf, n=100):
    return candles.get(ticker_tf, [])[-n:]
