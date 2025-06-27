import os
from pathlib import Path
import datetime
from tinydb import TinyDB, Query

# === Инициализация БД ===
DB_PATH = Path(__file__).parent.parent / "data" / "db.json"
os.makedirs(DB_PATH.parent, exist_ok=True)
db = TinyDB(DB_PATH)

# Таблицы
candle_table = db.table("candles")
signal_table = db.table("signals")
advanced_table = db.table("advanced_signals")

# === Временное хранилище в памяти ===
candles = {}  # {'GBPUSD_15S': [{...}, {...}]}
signals = {}  # {'GBPUSD_15S': [{...}, {...}]}
advanced_signals = {}  # {'GBPUSD_15S': [{...}, {...}]}

# === Загрузка из БД при старте ===
def load_from_db():
    print("[DB] Загрузка истории...")

    for item in candle_table.all():
        key = f"{item['ticker']}_{item['timeframe']}"
        candles.setdefault(key, []).append(item)

    for item in signal_table.all():
        key = f"{item['ticker']}_{item['timeframe']}"
        signals.setdefault(key, []).append(item)

    for item in advanced_table.all():
        key = f"{item['ticker']}_{item['timeframe']}"
        advanced_signals.setdefault(key, []).append(item)

    print(f"[DB] Загружено: {sum(len(v) for v in candles.values())} свечей, {sum(len(v) for v in signals.values())} сигналов, {sum(len(v) for v in advanced_signals.values())} advanced")

load_from_db()

# === Функция: Сохраняем свечу ===
def store_candle(data):
    key = f"{data['ticker']}_{data['timeframe']}"
    if key not in candles:
        candles[key] = []

    # Проверка на дубликаты по времени
    if any(c['time'] == data['time'] for c in candles[key]):
        return

    candle = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }

    candles[key].append(candle)
    candle_table.insert(candle)

    # Сортировка
    candles[key].sort(key=lambda x: x["time"])

# === Функция: Получить последние N свечей ===
def get_recent_candles(ticker_tf, n=100):
    return candles.get(ticker_tf, [])[-n:]

# === Функция: Сохраняем сигнал ===
def store_signal(data, advanced=False):
    key = f"{data['ticker']}_{data['timeframe']}"
    target = advanced_signals if advanced else signals
    table = advanced_table if advanced else signal_table

    signal_data = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data.get("time", datetime.datetime.utcnow().isoformat())
    }

    if advanced:
        signal_data["action"] = data["action"]
        signal_data["sltp"] = float(data.get("sltp", 0))
        signal_data["side"] = data.get("side", "flat")
    else:
        signal_data["action"] = data["action"]
        signal_data["contracts"] = float(data.get("contracts", 0))
        signal_data["position_size"] = float(data.get("position_size", 0))

    target.setdefault(key, []).append(signal_data)
    table.insert(signal_data)
