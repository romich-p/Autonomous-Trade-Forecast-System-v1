from flask import Flask, request, jsonify
from core.data_store import store_candle, store_signal
from core.predictor import make_prediction
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Вывод входящего JSON в лог Render
    app.logger.info("Received JSON: %s", data)

    if not data or "event" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    event_type = data["event"]

    if event_type == "candle":
        store_candle(data)
        prediction = make_prediction(data)
        return jsonify({"status": "candle stored", "prediction": prediction})

    elif event_type == "signal":
        store_signal(data)
        return jsonify({"status": "signal stored"})

    else:
        return jsonify({"error": "Unknown event type"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render задаёт порт через переменную окружения
    app.run(host="0.0.0.0", port=port)
