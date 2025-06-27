from flask import Flask, request, send_file, jsonify
from core.webhook_handler import handle_webhook
from core.data_store import candles, signals, advanced_signals
from core.visualize import visualize_plot
import io

app = Flask(__name__)

@app.route('/')
def index():
    return send_file("static/index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        payload = request.get_json()
        handle_webhook(payload)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"[ERROR] Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/plot')
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    
    key = f"{ticker}_{timeframe}".upper()
    if key not in candles:
        return jsonify({"status": "error", "message": "No data"}), 404

    img_bytes = visualize_plot(
        ticker,
        timeframe,
        candles[key],
        signals.get(key, []),
        advanced_signals.get(key, [])
    )
    
    return send_file(
        io.BytesIO(img_bytes),
        mimetype='image/png',
        as_attachment=False,
        download_name=f"{ticker}_{timeframe}.png"
    )

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
