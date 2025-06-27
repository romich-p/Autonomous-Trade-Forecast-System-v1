from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(data):
    if not isinstance(data, dict):
        print("[Webhook] Неверный формат JSON:", data)
        return

    event = data.get("event")
    ticker = data.get("ticker")
    timeframe = data.get("timeframe")

    if event == "candle":
        candle = data.get("candle")
        if candle:
            store_candle(ticker, timeframe, candle)

    elif event == "signal":
        signal = data.get("signal")
        if signal:
            store_signal(ticker, timeframe, signal)

    elif event == "advanced":
        adv = data.get("advanced")
        if adv:
            store_advanced(ticker, timeframe, adv)
