from core.data_store import load_database, save_database

def handle_webhook(payload):
    db = load_database()

    if db is None:
        db = {}

    ticker = payload.get("ticker")
    timeframe = payload.get("timeframe")

    if not ticker or not timeframe:
        print("[Webhook] Пропущен ticker или timeframe")
        return

    key = f"{ticker}_{timeframe}"
    if key not in db:
        db[key] = {"candles": [], "signals": [], "advanced": []}

    signal_type = payload.get("type")

    if signal_type == "candle":
        db[key]["candles"].append(payload)
    elif signal_type == "sma":
        db[key]["signals"].append(payload)
    elif signal_type == "technical":
        db[key]["advanced"].append(payload)
    else:
        print(f"[Webhook] Неизвестный тип данных: {signal_type}")
        return

    save_database(db)
    print(f"[Webhook] Обработан сигнал для {key} [{signal_type}]")
