import json
from flask import request, jsonify
from core.data_store import store_candle, store_signal, store_advanced


def handle_webhook(req):
    try:
        data = req.get_json(force=True)
        if not data:
            print("[ERROR] Webhook получил пустой JSON")
            return jsonify({"status": "error", "message": "Empty JSON"}), 400

        print(f"[Webhook] Получены данные: {json.dumps(data)[:500]}")

        if 'type' not in data:
            print("[ERROR] Webhook: нет ключа 'type'")
            return jsonify({"status": "error", "message": "Missing 'type'"}), 400

        event_type = data['type']

        if event_type == 'candle':
            ticker = data['ticker']
            timeframe = data['timeframe']
            candle = data['candle']
            store_candle(ticker, timeframe, candle)

        elif event_type == 'signal':
            ticker = data['ticker']
            timeframe = data['timeframe']
            signal = data['signal']
            store_signal(ticker, timeframe, signal)

        elif event_type == 'tp_sl':
            ticker = data['ticker']
            timeframe = data['timeframe']
            signal = data['signal']
            store_signal(ticker, timeframe, signal)

        elif event_type == 'advanced':
            ticker = data['ticker']
            timeframe = data['timeframe']
            adv = data['advanced']
            store_advanced(ticker, timeframe, adv)

        else:
            print(f"[ERROR] Webhook: неизвестный type '{event_type}'")
            return jsonify({"status": "error", "message": f"Unknown type: {event_type}"}), 400

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
