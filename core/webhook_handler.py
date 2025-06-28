import json
from flask import request
from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook():
    try:
        payload = request.get_json(force=True)
        if not payload:
            return {"status": "error", "message": "Empty payload"}, 400

        event_type = payload.get("event")
        ticker = payload.get("ticker", "").upper()
        timeframe = payload.get("timeframe", "").upper()

        if not ticker or not timeframe:
            return {"status": "error", "message": "Missing ticker or timeframe"}, 400

        if event_type == "candle":
            store_candle(ticker, timeframe, payload)
            print(f"[WEBHOOK] Candle received: {ticker} {timeframe}")
            return {"status": "ok"}

        elif event_type == "sma_cross":
            store_signal(ticker, timeframe, payload)
            print(f"[WEBHOOK] SMA signal received: {ticker} {timeframe}")
            return {"status": "ok"}

        elif event_type == "tp_sl":
            store_advanced(ticker, timeframe, payload)
            print(f"[WEBHOOK] Advanced signal received: {ticker} {timeframe}")
            return {"status": "ok"}

        else:
            print(f"[WEBHOOK] Unknown event type: {event_type}")
            return {"status": "error", "message": "Unknown event type"}, 400

    except Exception as e:
        print(f"[ERROR] Webhook exception: {e}")
        return {"status": "error", "message": str(e)}, 500

def handle_webhook(data):
    print("[Webhook] RAW DATA:", data)  # Добавь эту строку
    ...
