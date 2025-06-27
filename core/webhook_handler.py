from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(data):
    print("[WEBHOOK] Incoming:", data)

    data_type = data.get("type")
    ticker = data.get("ticker")
    timeframe = data.get("timeframe")

    if data_type == "candle":
        candle = data.get("candle")
        if ticker and timeframe and candle:
            print(f"[STORE] Saving candle for {ticker}_{timeframe}: {candle}")
            store_candle(ticker, timeframe, candle)
        else:
            print("[ERROR] Candle payload missing required fields.")
    elif data_type == "signal":
        signal = data.get("signal")
        if ticker and timeframe and signal:
            print(f"[STORE] Saving signal for {ticker}_{timeframe}: {signal}")
            store_signal(ticker, timeframe, signal)
        else:
            print("[ERROR] Signal payload missing required fields.")
    elif data_type == "tp_sl":
        signal = data.get("signal")
        if ticker and timeframe and signal:
            print(f"[STORE] Saving TP/SL signal for {ticker}_{timeframe}: {signal}")
            store_signal(ticker, timeframe, signal)
        else:
            print("[ERROR] TP/SL payload missing required fields.")
    elif data_type == "advanced":
        adv = data.get("adv")
        if ticker and timeframe and adv:
            print(f"[STORE] Saving advanced metrics for {ticker}_{timeframe}: {adv}")
            store_advanced(ticker, timeframe, adv)
        else:
            print("[ERROR] Advanced payload missing required fields.")
    else:
        print("[ERROR] Unknown webhook type:", data_type)
