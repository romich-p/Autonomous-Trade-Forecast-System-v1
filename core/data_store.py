import os
import json

DB_PATH = "db.json"

def load_data():
    if not os.path.exists(DB_PATH):
        print("[DB] db.json не найден, создаём новый файл")
        return {"candles": {}, "signals": {}, "advanced": {}}
    with open(DB_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("[DB] Ошибка чтения JSON — создаём новый")
            data = {"candles": {}, "signals": {}, "advanced": {}}
    print(f"[DB] Загружено: {len(data.get('candles', {}))} свечей, "
          f"{len(data.get('signals', {}))} сигналов, {len(data.get('advanced', {}))} advanced")
    return data

def save_data(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f)

def store_candle(data, timeframe, candle):
    ticker = candle["ticker"]
    tf = timeframe.upper()
    data.setdefault("candles", {}).setdefault(ticker, {}).setdefault(tf, []).append(candle)
    save_data(data)

def store_signal(data, signal):
    ticker = signal["ticker"]
    tf = signal["timeframe"].upper()
    data.setdefault("signals", {}).setdefault(ticker, {}).setdefault(tf, []).append(signal)
    save_data(data)

def store_advanced(data, advanced):
    ticker = advanced["ticker"]
    tf = advanced["timeframe"].upper()
    data.setdefault("advanced", {}).setdefault(ticker, {}).setdefault(tf, []).append(advanced)
    save_data(data)
