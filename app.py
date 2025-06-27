from flask import Flask, request, jsonify
from core.data_store import store_candle, store_signal
from core.predictor import make_prediction
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or "event" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    app.logger.info("Received JSON: %s", data)

    event_type = data["event"]

    if event_type == "candle":
        store_candle(data)
        prediction = make_prediction(data)
        return jsonify({"status": "candle stored", "prediction": prediction})

    elif event_type == "signal":
        store_signal(data, advanced=False)
        return jsonify({"status": "basic signal stored"})

    elif event_type == "signal_advanced":
        store_signal(data, advanced=True)
        return jsonify({"status": "advanced signal stored"})

    else:
        return jsonify({"error": "Unknown event type"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
