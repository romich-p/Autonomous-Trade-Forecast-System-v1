from flask import jsonify
from core.data_store import store_candle, store_signal, store_advanced

def handle_webhook(req):
    try:
        data = req.json
        if data.get("type") == "candle":
            store_candle(data["ticker"], data["timeframe"], data["candle"])
        elif data.get("type") == "signal":
            store_signal(data["ticker"], data["timeframe"], data["signal"])
        elif data.get("type") == "advanced":
            store_advanced(data["ticker"], data["timeframe"], data["advanced"])
        else:
            return jsonify({"status": "error", "message": "Unknown type"}), 400

        return jsonify({"status": "ok"})

    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
