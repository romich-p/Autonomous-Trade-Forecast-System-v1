# core/data_store.py
import json
import os
from collections import defaultdict

DB_FILE = "db.json"
candles = defaultdict(list)
signals = defaultdict(list)
advanced_signals = defaultdict(list)

def save_db():
    data = {
        "candles": candles,
        "signals": signals,
        "advanced_signals": advanced_signals
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            candles.update({k: v for k, v in data.get("candles", {}).items()})
            signals.update({k: v for k, v in data.get("signals", {}).items()})
            advanced_signals.update({k: v for k, v in data.get("advanced_signals", {}).items()})
            print(f"[DB] Загружено: {sum(len(v) for v in candles.values())} свечей, {sum(len(v) for v in signals.values())} сигналов, {sum(len(v) for v in advanced_signals.values())} advanced")
    else:
        print("[DB] db.json не найден, создаём новый файл")
        save_db()

def store_candle(ticker, timeframe, candle):
    key = f"{ticker}_{timeframe}".upper()
    print(f"[STORE_CANDLE] {key} → {candle}")
    candles[key].append(candle)
    save_db()

def store_signal(ticker, timeframe, signal):
    key = f"{ticker}_{timeframe}".upper()
    print(f"[STORE_SIGNAL] {key} → {signal}")
    signals[key].append(signal)
    save_db()

def store_advanced(ticker, timeframe, adv):
    key = f"{ticker}_{timeframe}".upper()
    print(f"[STORE_ADVANCED] {key} → {adv}")
    advanced_signals[key].append(adv)
    save_db()
