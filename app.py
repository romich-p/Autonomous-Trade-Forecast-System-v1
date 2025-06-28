from flask import Flask, request, send_file, jsonify
from core.data_store import store_candle, store_signal, store_advanced
from core.visualize import visualize_plot
from core.webhook_handler import handle_webhook
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('static/index.html')

@app.route('/plot')
def plot():
    ticker = request.args.get('ticker')
    timeframe = request.args.get('timeframe')

    from core.data_store import get_candles, get_signals, get_advanced_signals

    candles = get_candles(ticker, timeframe)
    signals = get_signals(ticker, timeframe)
    advanced_signals = get_advanced_signals(ticker, timeframe)

    if not candles:
        return jsonify({"status": "error", "message": "No data"}), 404

    img_bytes = visualize_plot(ticker, timeframe, candles, signals, advanced_signals)
    return send_file(img_bytes, mimetype='image/png')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        handle_webhook(data)
        return '', 200
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
