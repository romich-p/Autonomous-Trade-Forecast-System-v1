import json
from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(data):
    try:
        payload = json.loads(data)
    except Exception as e:
        return {"status": "error", "message": f"Invalid JSON: {e}"}

    if 'type' not in payload:
        return {"status": "error", "message": "Missing type in payload"}

    dtype = payload['type']

    if dtype == 'candle':
        try:
            ticker = payload['ticker']
            timeframe = payload['timeframe']
            candle = payload['candle']
            store_candle(ticker, timeframe, candle)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to store candle: {e}"}

    elif dtype == 'signal':
        try:
            ticker = payload['ticker']
            timeframe = payload['timeframe']
            signal = payload['signal']
            store_signal(ticker, timeframe, signal)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to store signal: {e}"}

    elif dtype == 'advanced':
        try:
            ticker = payload['ticker']
            timeframe = payload['timeframe']
            advanced = payload['advanced']
            store_advanced(ticker, timeframe, advanced)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to store advanced signal: {e}"}

    return {"status": "error", "message": f"Unknown type: {dtype}"}
