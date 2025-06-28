import json
from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(data):
    print(f"[Webhook] RAW DATA: {data}")
    event = data.get("event") or data.get("type")  # поддержка обоих форматов

    if event == "candle":
        candle = {
            "time": data.get("time") or data.get("timestamp"),
            "open": float(data["open"]),
            "high": float(data["high"]),
            "low": float(data["low"]),
            "close": float(data["close"]),
            "volume": float(data.get("volume", 0)),
        }
        print(f"[Webhook] Parsed Candle: {candle}")
        store_candle(data["ticker"], data["timeframe"], candle)
        print(f"[Webhook] Candle stored ✅")

    elif event == "signal":
        signal = {
            "time": data["time"],
            "direction": data["direction"]
        }
        store_signal(data["ticker"], data["timeframe"], signal)
        print(f"[Webhook] Signal stored ✅")

    elif event == "signal_advanced":
        advanced = {
            "time": data["time"],
            "action": data["action"],
            "side": data["side"],
            "sltp": float(data.get("sltp", 0)),
        }
        store_advanced(data["ticker"], data["timeframe"], advanced)
        print(f"[Webhook] Advanced signal stored ✅")

    else:
        print(f"[Webhook] Unknown event: {event}")
