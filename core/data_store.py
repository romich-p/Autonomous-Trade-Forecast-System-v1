import os
import datetime
from tinydb import TinyDB, Query

# === Пути и инициализация базы ===
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/db.json")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # создаём директорию, если не существует
db = TinyDB(DB_PATH)

# === Ключи для хранения в TinyDB ===
CANDLES_TABLE = "candles"
SIGNALS_TABLE = "signals"
ADV_SIGNALS_TABLE = "advanced_signals"

# === Поддерживаемые таймфреймы ===
SKIP_TIMEFRAMES = {"5S", "45S", "10m"}


def _tf_key(ticker, timeframe):
    return f"{ticker}_{timeframe}"


# === Хранилище в памяти ===
candles = {}
signals = {}
advanced_signals = {}

# === Функция: Сохраняем свечу ===
def store_candle(data):
    tf = data["timeframe"]
    if tf in SKIP_TIMEFRAMES:
        return

    key = _tf_key(data["ticker"], tf)
    entry = {
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    }

    # В память
    candles.setdefault(key, [])
    if any(c["time"] == entry["time"] for c in candles[key]):
        return
    candles[key].append(entry)
    candles[key].sort(key=lambda x: x["time"])

    # В базу
    db.table(CANDLES_TABLE).insert({**entry, "key": key})


# === Функция: Получаем последние N свечей ===
def get_recent_candles(ticker_tf, n=100):
    return candles.get(ticker_tf, [])[-n:]


# === Функция: Сохраняем сигнал ===
def store_signal(data, advanced=False):
    tf = data["timeframe"]
    if tf in SKIP_TIMEFRAMES:
        return

    key = _tf_key(data["ticker"], tf)
    time = data.get("time", datetime.datetime.utcnow().isoformat())
    record = {
        "ticker": data["ticker"],
        "timeframe": tf,
        "time": time,
        "action": data["action"],
    }

    if advanced:
        record["sltp"] = float(data.get("sltp", 0))
        record["side"] = data.get("side", "flat")
        advanced_signals.setdefault(key, []).append(record)
        db.table(ADV_SIGNALS_TABLE).insert({**record, "key": key})
    else:
        record["contracts"] = float(data.get("contracts", 0))
        record["position_size"] = float(data.get("position_size", 0))
        signals.setdefault(key, []).append(record)
        db.table(SIGNALS_TABLE).insert({**record, "key": key})


# === Функция: Загрузка из базы при старте ===
def load_from_db():
    for row in db.table(CANDLES_TABLE).all():
        key = row["key"]
        candles.setdefault(key, []).append({
            "time": row["time"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row.get("volume", 0),
        })

    for row in db.table(SIGNALS_TABLE).all():
        key = _tf_key(row["ticker"], row["timeframe"])
        signals.setdefault(key, []).append(row)

    for row in db.table(ADV_SIGNALS_TABLE).all():
        key = _tf_key(row["ticker"], row["timeframe"])
        advanced_signals.setdefault(key, []).append(row)


# Загружаем при старте
load_from_db()
