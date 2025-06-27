from flask import Flask, request, jsonify, send_file
from core.webhook_handler import handle_webhook
from core.data_store import load_data, store_candle, store_signal, store_advanced
from core.visualize import visualize_plot

app = Flask(__name__)

# Загружаем данные из db.json
data = load_data()

@app.route("/")
def index():
    return send_file("frontend/index.html")

@app.route("/plot")
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    if not ticker or not timeframe:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    candles = data.get("candles", {}).get(ticker, {}).get(timeframe.upper(), [])
    signals = data.get("signals", {}).get(ticker, {}).get(timeframe.upper(), [])
    advanced = data.get("advanced", {}).get(ticker, {}).get(timeframe.upper(), [])

    if not candles:
        return jsonify({"status": "error", "message": "No data"}), 404

    # Визуализируем
    output_path = visualize_plot(ticker, timeframe, candles, signals, advanced)
    return send_file(output_path, mimetype="image/png")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        payload = request.json
        handle_webhook(payload, data)
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, port=10000, host="0.0.0.0")
