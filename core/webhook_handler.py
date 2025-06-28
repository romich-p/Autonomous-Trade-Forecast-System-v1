from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(data):
    if 'type' not in data:
        return {"status": "error", "message": "Missing type"}
    
    data_type = data['type']
    ticker = data.get('ticker', 'GBPUSD')  # по умолчанию
    timeframe = data.get('timeframe', '15S')

    if data_type == 'candle':
        store_candle(ticker, timeframe, data['data'])
    elif data_type == 'signal':
        store_signal(data)
    elif data_type == 'advanced':
        store_advanced(data)
    else:
        return {"status": "error", "message": "Unknown type"}

    return {"status": "ok"}
