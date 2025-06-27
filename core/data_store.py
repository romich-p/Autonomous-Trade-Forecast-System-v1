import os
import datetime
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

# === Настройки ===
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# === TinyDB init ===
db = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage))
candles_table = db.table("candles")
signals_table = db.table("signals")
advanced_table = db.table("advanced_signals")

# === Оперативное хранилище ===
candles = {}  # {'GBPUSD_15S': [ {...}, {...} ]}
signals = {}  # {'GBPUSD_15S': [ {...}, {...} ]}
advanced_signals = {}  # {'GBPUSD_15S': [ {...}, {...} ]}

# === Загрузка из базы при старте ===
for item in candles_table.all():
    key = item["key"]
    candles.setdefault(key, []).append(item["data"])

for item in signals_table.all():
    key = item["key"]
    signals.setdefault(key, []).append(item["data"])

for item in advanced_table.all():
    key = item["key"]
    advanced_signals.setdefault(key, []).append(item["data"])

# === Сохраняем свечу ===
def store_candle(data):
    key = f"{data['ticker']}_{data['timeframe']}"
    if key not in candles:
        candles[key] = []

    if any(c['time'] == data['time'] for c in candles[key]):
        print(f"[SKIP] Duplicate candle {key} @ {data['time']}")
        return

    entry = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }

    candles[key].append(entry)
    candles[key].sort(key=lambda x: x["time"])
    candles_table.insert({"key": key, "data": entry})
    print(f"[CANDLE] Stored {key} @ {data['time']}")

# === Получить последние N свечей ===
def get_recent_candles(ticker_tf, n=100):
    return candles.get(ticker_tf, [])[-n:]

# === Сохраняем сигнал ===
def store_signal(data, advanced=False):
    key = f"{data['ticker']}_{data['timeframe']}"
    target = advanced_signals if advanced else signals
    table = advanced_table if advanced else signals_table

    signal_data = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data.get("time", datetime.datetime.utcnow().isoformat())
    }

    if advanced:
        signal_data["action"] = data["action"]
        signal_data["sltp"] = float(data.get("sltp", 0))
        signal_data["side"] = data.get("side", "flat")
    else:
        signal_data["action"] = data["action"]
        signal_data["contracts"] = float(data.get("contracts", 0))
        signal_data["position_size"] = float(data.get("position_size", 0))

    target.setdefault(key, []).append(signal_data)
    table.insert({"key": key, "data": signal_data})
    print(f"[SIGNAL] {'ADV' if advanced else 'BASIC'} {key} @ {signal_data['time']}")
