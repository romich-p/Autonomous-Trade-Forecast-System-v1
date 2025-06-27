from flask import Flask, request, send_file, render_template
from core.webhook_handler import handle_webhook
from core.plotter import plot_chart
from core.data_store import load_database

app = Flask(__name__)

# Загружаем базу при старте
load_database()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        handle_webhook(data)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route("/plot", methods=["GET"])
def plot():
    ticker = request.args.get("ticker")
    timeframe = request.args.get("timeframe")
    image_path = plot_chart(ticker, timeframe)
    if image_path and os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    return {"status": "error", "message": "No data"}, 404

if __name__ == "__main__":
    app.run(debug=False, port=10000, host="0.0.0.0")
