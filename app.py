from flask import Flask, request, jsonify, send_file
from core.webhook_handler import handle_webhook
from core.data_store import (
    get_candles,
    get_signals,
    get_advanced_signals,
    load_database,
    save_database,
)
from core.visualize import visualize_plot
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        payload = request.json
        handle_webhook(payload)
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/plot")
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    if not ticker or not timeframe:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    candles = get_candles(ticker, timeframe)
    signals = get_signals(ticker, timeframe)
    advanced_signals = get_advanced_signals(ticker, timeframe)

    if not candles:
        return jsonify({"status": "error", "message": "No data"}), 404

    img_bytes = visualize_plot(ticker, timeframe, candles, signals, advanced_signals)
    return send_file(img_bytes, mimetype="image/png")

@app.route("/status")
def status():
    db = load_database()
    summary = []

    for key, records in db.items():
        n_candles = len(records.get("candles", []))
        n_signals = len(records.get("signals", []))
        n_advanced = len(records.get("advanced", []))
        summary.append({
            "key": key,
            "candles": n_candles,
            "signals": n_signals,
            "advanced": n_advanced,
        })

    return jsonify({"status": "ok", "pairs": summary})

@app.route("/")
def index():
    return send_file("static/index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
