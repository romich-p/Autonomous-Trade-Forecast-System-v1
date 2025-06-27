import json
import os
from datetime import datetime
from collections import defaultdict

DB_FILE = "db.json"

# Структура хранилища в памяти
db = {
    "candles": defaultdict(list),
    "signals": defaultdict(list),
    "advanced": defaultdict(list),
}

# Загрузка данных с диска
def load_db():
    if not os.path.exists(DB_FILE):
        print("[DB] db.json не найден, создаём новый файл")
        return

    try:
        with open(DB_FILE, "r") as f:
            raw = json.load(f)
            db["candles"] = defaultdict(list, {
                k: v for k, v in raw.get("candles", {}).items()
            })
            db["signals"] = defaultdict(list, {
                k: v for k, v in raw.get("signals", {}).items()
            })
            db["advanced"] = defaultdict(list, {
                k: v for k, v in raw.get("advanced", {}).items()
            })
            print(f"[DB] Загружено: {sum(len(v) for v in db['candles'].values())} свечей, {sum(len(v) for v in db['signals'].values())} сигналов, {sum(len(v) for v in db['advanced'].values())} advanced")
    except Exception as e:
        print("[DB] Ошибка при загрузке:", e)

# Сохранение данных на диск
def save_db():
    try:
        with open(DB_FILE, "w") as f:
            json.dump({
                "candles": db["candles"],
                "signals": db["signals"],
                "advanced": db["advanced"],
            }, f)
    except Exception as e:
        print("[DB] Ошибка при сохранении:", e)

# Вернуть данные по тикеру и ТФ
def get_data_by_pair_and_tf(ticker, timeframe):
    key = f"{ticker}_{timeframe}"
    return (
        db["candles"].get(key, []),
        db["signals"].get(key, []),
        db["advanced"].get(key, []),
    )

def store_candle(ticker, timeframe, candle):
    key = f"{ticker}_{timeframe}"
    db["candles"][key].append(candle)
    save_db()

def store_signal(ticker, timeframe, signal):
    key = f"{ticker}_{timeframe}"
    db["signals"][key].append(signal)
    save_db()

def store_advanced(ticker, timeframe, advanced):
    key = f"{ticker}_{timeframe}"
    db["advanced"][key].append(advanced)
    save_db()

# Загружаем базу при старте
load_db()
