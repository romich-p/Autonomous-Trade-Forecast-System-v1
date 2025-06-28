# app.py
from flask import Flask, request, send_file, jsonify
from core.webhook_handler import handle_webhook
from core.data_store import get_candles, get_signals, get_advanced_signals
from core.visualize import visualize_plot
import io

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        handle_webhook(data)
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/plot")
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    
    candles = get_candles(ticker, timeframe)
    signals = get_signals(ticker, timeframe)
    advanced_signals = get_advanced_signals(ticker, timeframe)

    if not candles:
        return jsonify({"status": "error", "message": "No data"}), 404

    img_bytes = visualize_plot(ticker, timeframe, candles, signals, advanced_signals)
    return send_file(io.BytesIO(img_bytes), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
