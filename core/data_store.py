import os
import datetime
from tinydb import TinyDB, Query
from tinydb.table import Document

# Убедимся, что папка data существует
DB_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DB_DIR, exist_ok=True)

# Путь к файлу базы
DB_PATH = os.path.join(DB_DIR, "db.json")
db = TinyDB(DB_PATH)

# === Хранилища в памяти ===
candles = {}
signals = {}
advanced_signals = {}

# === Загрузка из базы при старте ===
def load_data():
    global candles, signals, advanced_signals

    # Загрузка свечей
    for row in db.table("candles").all():
        key = row["key"]
        if key not in candles:
            candles[key] = []
        candles[key].append(row["data"])
        candles[key].sort(key=lambda x: x["time"])

    # Загрузка простых сигналов
    for row in db.table("signals").all():
        key = row["key"]
        if key not in signals:
            signals[key] = []
        signals[key].append(row["data"])

    # Загрузка расширенных сигналов
    for row in db.table("advanced_signals").all():
        key = row["key"]
        if key not in advanced_signals:
            advanced_signals[key] = []
        advanced_signals[key].append(row["data"])

# === Функция: Сохраняем свечу ===
def store_candle(data):
    key = f"{data['ticker']}_{data['timeframe']}"
    if key not in candles:
        candles[key] = []

    if any(c['time'] == data['time'] for c in candles[key]):
        return

    candle = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }
    candles[key].append(candle)
    candles[key].sort(key=lambda x: x["time"])

    db.table("candles").insert({"key": key, "data": candle})

# === Функция: Сохраняем сигнал ===
def store_signal(data, advanced=False):
    key = f"{data['ticker']}_{data['timeframe']}"
    signal_data = {
        "time": data.get("time", datetime.datetime.utcnow().isoformat()),
        "action": data["action"]
    }

    if advanced:
        signal_data["side"] = data.get("side", "flat")
        signal_data["sltp"] = float(data.get("sltp", 0))
        if key not in advanced_signals:
            advanced_signals[key] = []
        advanced_signals[key].append(signal_data)
        db.table("advanced_signals").insert({"key": key, "data": signal_data})
    else:
        signal_data["contracts"] = float(data.get("contracts", 0))
        signal_data["position_size"] = float(data.get("position_size", 0))
        if key not in signals:
            signals[key] = []
        signals[key].append(signal_data)
        db.table("signals").insert({"key": key, "data": signal_data})

# Загрузить данные при запуске
load_data()
