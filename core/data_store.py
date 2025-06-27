import json
from collections import defaultdict
from datetime import datetime

# Хранилища
candles = defaultdict(list)
signals = defaultdict(list)


def normalize_action(data):
    action = data.get("action")
    sltp = float(data.get("sltp", 0))
    side = data.get("side", "flat")

    if action == "tp_sl":
        if sltp != 0 and side in ("long", "short"):
            return side  # вход в позицию
        elif sltp == 0 and side == "flat":
            return "tp_sl"  # выход из позиции
    return action


def store_candle(data):
    key = (data["ticker"], data["timeframe"])
    timestamp = data["time"]

    # Удаление дубликатов по времени
    if any(candle["time"] == timestamp for candle in candles[key]):
        return

    candle = {
        "time": timestamp,
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
    }
    candles[key].append(candle)
    candles[key] = sorted(candles[key], key=lambda x: x["time"])  # сортировка по времени


def store_signal(data, advanced=False):
    key = (data["ticker"], data["timeframe"])

    if advanced:
        action = normalize_action(data)
        signal = {
            "time": data["time"],
            "action": action,
            "sltp": float(data.get("sltp", 0)),
            "side": data.get("side", "flat")
        }
    else:
        signal = {
            "time": data["time"],
            "action": data["action"],
            "contracts": data.get("contracts"),
            "position_size": data.get("position_size"),
        }

    signals[key].append(signal)
    signals[key] = sorted(signals[key], key=lambda x: x["time"])  # сортировка


def get_recent_candles(ticker, timeframe, limit=50):
    return candles[(ticker, timeframe)][-limit:]
