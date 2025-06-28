# core/data_store.py

import os
import json
from tinydb import TinyDB, Query

DB_PATH = "db.json"
db_dir = os.path.dirname(DB_PATH)

# Создаём директорию, если указана и не пуста
if db_dir:
    os.makedirs(db_dir, exist_ok=True)

db = TinyDB(DB_PATH)

candles_table = db.table("candles")
signals_table = db.table("signals")
advanced_table = db.table("advanced")


def store_candle(ticker, timeframe, candle):
    candles_table.insert({
        "ticker": ticker,
        "timeframe": timeframe,
        "candle": candle
    })


def store_signal(ticker, timeframe, signal):
    signals_table.insert({
        "ticker": ticker,
        "timeframe": timeframe,
        "signal": signal
    })


def store_advanced(ticker, timeframe, signal):
    advanced_table.insert({
        "ticker": ticker,
        "timeframe": timeframe,
        "signal": signal
    })


def get_candles(ticker, timeframe):
    Candle = Query()
    return [
        item["candle"]
        for item in candles_table.search((Candle.ticker == ticker) & (Candle.timeframe == timeframe))
    ]


def get_signals(ticker, timeframe):
    Signal = Query()
    return [
        item["signal"]
        for item in signals_table.search((Signal.ticker == ticker) & (Signal.timeframe == timeframe))
    ]


def get_advanced_signals(ticker, timeframe):
    Adv = Query()
    return [
        item["signal"]
        for item in advanced_table.search((Adv.ticker == ticker) & (Adv.timeframe == timeframe))
    ]
