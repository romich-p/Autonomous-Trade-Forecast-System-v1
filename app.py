from flask import Flask, request, jsonify
from core.data_store import store_candle, store_signal
from core.predictor import make_prediction
from core.plotter import plot_chart
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "✅ Autonomous Trade Forecast System is running."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    app.logger.info("Received JSON: %s", data)

    if not data or "event" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    event_type = data["event"]

    try:
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

    except Exception as e:
        app.logger.error("Exception on /webhook: %s", str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/plot', methods=['GET'])
def plot():
    ticker = request.args.get("ticker", "GBPUSD")
    tf = request.args.get("timeframe", "15S")
    return plot_chart(ticker, tf)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
