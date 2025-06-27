from flask import Flask, request, send_file, render_template
from core.data_store import store_candle, store_signal, store_advanced
from core.plotter import plot_chart

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        ticker = data["ticker"]
        timeframe = data["timeframe"]
        signal_type = data["type"]

        if signal_type == "candle":
            store_candle(ticker, timeframe, data["data"])
        elif signal_type == "signal":
            store_signal(ticker, timeframe, data["data"])
        elif signal_type == "tp_sl":
            store_advanced(ticker, timeframe, data["data"])
        else:
            return "Unknown signal type", 400

        return "ok", 200
    except Exception as e:
        print(f"[Webhook ERROR] {e}")
        return f"Error: {e}", 500

@app.route("/plot")
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    try:
        image_path = plot_chart(ticker, timeframe)
        if image_path:
            return send_file(image_path, mimetype="image/png")
        else:
            return "No data", 404
    except Exception as e:
        print(f"[Plot ERROR] {e}")
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
