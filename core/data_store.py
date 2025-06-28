import os
import json
from tinydb import TinyDB, Query
from datetime import datetime

db_path = 'db.json'
db = TinyDB(db_path)

def store_candle(ticker, timeframe, candle):
    db.table('candles').insert({'ticker': ticker, 'timeframe': timeframe, **candle})

def store_signal(signal):
    db.table('signals').insert(signal)

def store_advanced(signal):
    db.table('advanced').insert(signal)

def load_candles(ticker, timeframe):
    return db.table('candles').search((Query().ticker == ticker) & (Query().timeframe == timeframe))

def load_signals(ticker, timeframe):
    return db.table('signals').search((Query().get('ticker') == ticker) & (Query().get('timeframe') == timeframe))

def load_advanced(ticker, timeframe):
    return db.table('advanced').search((Query().get('ticker') == ticker) & (Query().get('timeframe') == timeframe))
