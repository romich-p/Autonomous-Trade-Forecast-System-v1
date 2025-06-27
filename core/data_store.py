import os
import json
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def store_candle(data):
    ticker = data["ticker"]
    tf = data["timeframe"]
    date = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{DATA_DIR}/{ticker}_{tf}_{date}_candles.jsonl"

    candle = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
    }

    if "volume" in data:
        candle["volume"] = float(data["volume"])

    with open(filename, "a") as f:
        f.write(json.dumps(candle) + "\n")

def store_signal(data, advanced=False):
    ticker = data["ticker"]
    tf = data["timeframe"]
    date = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{DATA_DIR}/{ticker}_{tf}_{date}_signals.jsonl"

    raw_action = data.get("action", "").lower()
    action = "tp_sl" if raw_action == "close" else raw_action

    signal = {
        "time": data["time"],
        "action": action
    }

    if "sltp" in data:
        try:
            signal["sltp"] = float(data["sltp"])
        except ValueError:
            pass

    if not advanced:
        signal["position_size"] = data.get("position_size")
        signal["contracts"] = data.get("contracts")

    with open(filename, "a") as f:
        f.write(json.dumps(signal) + "\n")

def get_recent_candles(ticker, timeframe, limit=50):
    return []
