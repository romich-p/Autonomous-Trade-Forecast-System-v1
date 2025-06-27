# core/db.py
from tinydb import TinyDB, Query
import os

# Путь к файлу БД
os.makedirs("db", exist_ok=True)
db_path = os.path.join("db", "signals.json")
db = TinyDB(db_path)

Signal = Query()

def save_signal(signal):
    db.insert(signal)

def get_signals(ticker, timeframe):
    return db.search((Signal.ticker == ticker) & (Signal.timeframe == timeframe))
