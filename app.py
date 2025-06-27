from flask import Flask, request, jsonify, send_file
from core.webhook_handler import handle_webhook
from core.data_store import get_data_by_pair_and_tf
from visualize import visualize_plot
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('static/index.html')

@app.route('/plot')
def plot():
    ticker = request.args.get('ticker')
    timeframe = request.args.get('timeframe')
    key = f"{ticker}_{timeframe}"
    print(f"[PLOT] Requested: {key}")

    candles, signals, advanced = get_data_by_pair_and_tf(ticker, timeframe)
    if not candles:
        print(f"[PLOT] No data for {key}")
        return jsonify({"status": "error", "message": "No data"}), 404

    filepath = visualize_plot(ticker, timeframe, candles, signals, advanced)
    return send_file(filepath, mimetype='image/png')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        payload = request.get_json(force=True)
        print(f"[WEBHOOK] Raw payload: {payload}")
        if payload:
            print(f"[WEBHOOK] Keys: {list(payload.keys())}")
        handle_webhook(payload)
        return jsonify({'status': 'ok'})
    except Exception as e:
        print("[ERROR in /webhook]:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
