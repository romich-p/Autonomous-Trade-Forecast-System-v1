<вставим позже>from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(data: dict):
    if not data or "type" not in data:
        raise ValueError("Invalid webhook data")

    typ = data["type"]
    ticker = data.get("ticker", "UNKNOWN")
    timeframe = data.get("timeframe", "1m")

    if typ == "candle":
        candle = data["data"]
        store_candle(ticker, timeframe, candle)

    elif typ == "signal":
        signal = {
            "time": data["time"],
            "action": data["action"],
            "strategy": data.get("strategy", "unknown")
        }
        store_signal(ticker, timeframe, signal)

    elif typ == "tp_sl":
        advanced = {
            "time": data["time"],
            "side": data["side"]
        }
        store_advanced(ticker, timeframe, advanced)

    else:
        raise ValueError(f"Unknown type: {typ}")
