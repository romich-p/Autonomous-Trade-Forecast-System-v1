from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(data):
    """
    Обрабатывает входящие данные от TradingView через вебхук.
    """
    if "type" not in data or "ticker" not in data or "timeframe" not in data:
        return "Invalid payload", 400

    event_type = data["type"]
    ticker = data["ticker"]
    timeframe = data["timeframe"]

    if event_type == "candle":
        candle = data.get("candle")
        if not candle:
            return "Missing candle data", 400
        store_candle(ticker, timeframe, candle)

    elif event_type == "signal":
        signal = data.get("signal")
        if not signal:
            return "Missing signal data", 400
        store_signal(ticker, timeframe, signal)

    elif event_type == "advanced":
        adv_signal = data.get("signal")
        if not adv_signal:
            return "Missing advanced signal", 400
        store_advanced(ticker, timeframe, adv_signal)

    else:
        return "Unknown type", 400

    return "OK", 200
