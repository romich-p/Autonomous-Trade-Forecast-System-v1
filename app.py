from flask import Flask, request, jsonify, send_file
from core.data_store import load_data, store_candle, store_signal, store_advanced
from core.visualize import visualize_plot
from core.webhook_handler import handle_webhook

app = Flask(__name__)

# Загрузка истории
print("[DB] Загрузка истории...")
load_data()

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/plot")
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    if not ticker or not timeframe:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    img_bytes = visualize_plot(ticker, timeframe)
    if img_bytes is None:
        return jsonify({"status": "error", "message": "No data"}), 404

    return send_file(img_bytes, mimetype="image/png")

@app.route("/webhook", methods=["POST"])
def webhook():
    return handle_webhook(request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
