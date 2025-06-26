import json
import os
from collections import defaultdict

# Хранилище в памяти — просто списки
candles = defaultdict(lambda: defaultdict(list))   # candles[ticker][tf]
signals = defaultdict(list)                        # signals[ticker]

DATA_PATH = "logs"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def store_candle(data):
    ticker = data["ticker"]
    tf = data["timeframe"]

    candle = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data["volume"])
    }

    candles[ticker][tf].append(candle)

    # Сохраняем
    ensure_dir(DATA_PATH)
    path = os.path.join(DATA_PATH, f"{ticker}_{tf}_candles.json")
    with open(path, "w") as f:
        json.dump(candles[ticker][tf], f, indent=2)

def store_signal(data):
    ticker = data["ticker"]
    signal = {
        "time": data.get("time"),
        "timeframe": data.get("timeframe"),
        "action": data.get("action"),
        "contracts": int(data.get("contracts", 0)),
        "position_size": float(data.get("position_size", 0.0))
    }

    signals[ticker].append(signal)

    ensure_dir(DATA_PATH)
    path = os.path.join(DATA_PATH, f"{ticker}_signals.json")
    with open(path, "w") as f:
        json.dump(signals[ticker], f, indent=2)

def get_recent_candles(ticker, tf, count=None):
    data = candles[ticker][tf]
    return data if count is None else data[-count:]