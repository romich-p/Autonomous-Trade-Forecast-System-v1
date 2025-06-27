import datetime
from tinydb import TinyDB, Query
import os

# === Инициализация базы ===
db_path = os.path.join(os.path.dirname(__file__), "../db/signals.json")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
db = TinyDB(db_path)

# === Хранилище в памяти ===
candles = {}  # (ticker, timeframe) -> [candles]
signals = {}  # (ticker, timeframe) -> [simple signals]
advanced_signals = {}  # (ticker, timeframe) -> [advanced signals]

# === Сохраняем свечу ===
def store_candle(data):
    key = (data['ticker'], data['timeframe'])
    if key not in candles:
        candles[key] = []

    if any(c['time'] == data['time'] for c in candles[key]):
        return

    candles[key].append({
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    })

    candles[key].sort(key=lambda x: x["time"])

# === Получить последние N свечей ===
def get_recent_candles(ticker_tf, n=100):
    return candles.get(ticker_tf, [])[-n:]

# === Сохраняем сигнал (и в память, и в файл) ===
def store_signal(data, advanced=False):
    key = (data["ticker"], data["timeframe"])
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
    else:
        signal_data["contracts"] = float(data.get("contracts", 0))
        signal_data["position_size"] = float(data.get("position_size", 0))

    target[key].append(signal_data)

    # Сохраняем в файл
    db.insert({**signal_data, "advanced": advanced})
