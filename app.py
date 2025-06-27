from flask import Flask, request, send_file, jsonify
import io
from core.data_store import load_data
from core.visualize import visualize_plot
from core.webhook_handler import handle_webhook

app = Flask(__name__)
candles, signals, advanced_signals = load_data()

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/plot")
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    if not ticker or not timeframe:
        return jsonify({"status": "error", "message": "Missing ticker or timeframe"}), 400

    key = (ticker, timeframe)
    if key not in candles or key not in signals or key not in advanced_signals:
        return jsonify({"status": "error", "message": "No data"}), 404

    img_bytes = visualize_plot(ticker, timeframe, candles, signals, advanced_signals)
    return send_file(io.BytesIO(img_bytes), mimetype='image/png')

@app.route("/webhook", methods=["POST"])
def webhook():
    result = handle_webhook(request.data)
    status_code = 200 if result.get("status") == "success" else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
