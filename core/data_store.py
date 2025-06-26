import json
import os
from datetime import datetime

# Папка для хранения свечей и сигналов
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def store_candle(data):
    ticker = data["ticker"]
    tf = data["timeframe"]
    date = datetime.utcnow().strftime("%Y-%m-%d")

    filename = f"{DATA_DIR}/{ticker}_{tf}_{date}_candles.jsonl"
    with open(filename, "a") as f:
        f.write(json.dumps({
            "time": data["time"],
            "open": float(data["open"]),
            "high": float(data["high"]),
            "low": float(data["low"]),
            "close": float(data["close"]),
            "volume": float(data.get("volume", 0))  # безопасно, даже если volume нет
        }) + "\n")

def store_signal(data):
    ticker = data["ticker"]
    tf = data["timeframe"]
    date = datetime.utcnow().strftime("%Y-%m-%d")

    filename = f"{DATA_DIR}/{ticker}_{tf}_{date}_signals.jsonl"
    with open(filename, "a") as f:
        f.write(json.dumps({
            "time": data["time"],
            "action": data["action"],
            "position_size": data["position_size"],
            "contracts": data["contracts"]
        }) + "\n")
