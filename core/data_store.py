import os
import json
from datetime import datetime

# Хранилище данных
candles = {}  # структура: {"GBPUSD": {"15S": [ ... ]}}
signals = []

def parse_time(t):
    return datetime.fromisoformat(t.replace("Z", "+00:00"))

def store_candle(data):
    symbol = data["ticker"]
    tf = data["timeframe"]
    ts = parse_time(data["time"])

    if symbol not in candles:
        candles[symbol] = {}
    if tf not in candles[symbol]:
        candles[symbol][tf] = []

    new_candle = {
        "time": ts,
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
    }

    # Удаляем дубликаты и сортируем по времени
    existing = candles[symbol][tf]
    candles[symbol][tf] = sorted(
        [c for c in existing if c["time"] != ts] + [new_candle],
        key=lambda x: x["time"]
    )

def normalize_action(data):
    action = data.get("action")
    sltp = float(data.get("sltp", 0))
    side = data.get("side", "flat")

    # Обработка TP/SL при входящем действии buy/sell
    if action in ("buy", "sell") and sltp == 0 and side == "flat":
        return "tp_sl"
    return action

def store_signal(data, advanced=False):
    symbol = data["ticker"]
    tf = data["timeframe"]
    ts = parse_time(data["time"])

    signal = {
        "symbol": symbol,
        "timeframe": tf,
        "time": ts,
        "advanced": advanced
    }

    if advanced:
        signal.update({
            "action": normalize_action(data),
            "sltp": float(data.get("sltp", 0)),
            "side": data.get("side", "flat")
        })
    else:
        signal.update({
            "action": data.get("action"),
            "contracts": float(data.get("contracts", 0)),
            "position_size": float(data.get("position_size", 0))
        })

    signals.append(signal)

def get_recent_candles(symbol, tf, lookback=100):
    if symbol in candles and tf in candles[symbol]:
        return candles[symbol][tf][-lookback:]
    return []
