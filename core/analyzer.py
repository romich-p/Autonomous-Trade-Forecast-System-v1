import datetime
from tinydb import TinyDB, Query
import os

# === Константы ===
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
EXCLUDED_TIMEFRAMES = {"5S", "45S", "10M"}

# === Инициализация базы ===
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
db = TinyDB(DB_PATH)
tb_candles = db.table("candles")
tb_signals = db.table("signals")
tb_advanced = db.table("advanced_signals")

# === ОЗУ-кэш ===
candles = {}
signals = {}
advanced_signals = {}

# === Сохраняем свечу ===
def store_candle(data):
    if data["timeframe"] in EXCLUDED_TIMEFRAMES:
        return

    key = f"{data['ticker']}_{data['timeframe']}"
    if key not in candles:
        candles[key] = []

    if any(c["time"] == data["time"] for c in candles[key]):
        return

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
    tb_candles.insert({"key": key, **record})

# === Сохраняем сигнал ===
def store_signal(data, advanced=False):
    if data["timeframe"] in EXCLUDED_TIMEFRAMES:
        return

    key = f"{data['ticker']}_{data['timeframe']}"
    target = advanced_signals if advanced else signals
    if key not in target:
        target[key] = []

    signal_data = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data.get("time", datetime.datetime.utcnow().isoformat()),
        "action": data["action"]
    }

    if advanced:
        signal_data["sltp"] = float(data.get("sltp", 0))
        signal_data["side"] = data.get("side", "flat")
        tb_advanced.insert(signal_data)
    else:
        signal_data["contracts"] = float(data.get("contracts", 0))
        signal_data["position_size"] = float(data.get("position_size", 0))
        tb_signals.insert(signal_data)

    target[key].append(signal_data)

# === Восстановление данных ===
def preload_memory():
    for row in tb_candles:
        key = row["key"]
        record = {
            "time": row["time"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row["volume"]
        }
        candles.setdefault(key, []).append(record)

    for row in tb_signals:
        key = f"{row['ticker']}_{row['timeframe']}"
        signals.setdefault(key, []).append(row)

    for row in tb_advanced:
        key = f"{row['ticker']}_{row['timeframe']}"
        advanced_signals.setdefault(key, []).append(row)

preload_memory()
