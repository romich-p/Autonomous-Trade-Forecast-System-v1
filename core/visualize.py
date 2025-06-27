import io
import base64
import matplotlib.pyplot as plt
from analyzer import analyze_candles

def visualize_plot(ticker, timeframe, candles, signals, advanced):
    if not candles:
        return {"status": "error", "message": "No candle data"}

    times = [c["timestamp"] for c in candles]
    prices = [c["close"] for c in candles]

    plt.figure(figsize=(10, 4))
    plt.plot(times, prices, label="Close", linewidth=1.5)

    for sig in signals:
        ts = sig["timestamp"]
        side = sig.get("side", "")
        if side == "long":
            plt.axvline(x=ts, color="green", linestyle="--", alpha=0.5)
        elif side == "short":
            plt.axvline(x=ts, color="red", linestyle="--", alpha=0.5)
        elif side == "flat":
            plt.axvline(x=ts, color="gray", linestyle="--", alpha=0.3)

    analysis = analyze_candles(ticker, timeframe, candles, signals, advanced)
    label = f"{ticker} {timeframe} — Trend: {analysis['trend']}, Entry: {analysis['entry']}%, Prob: {analysis['probability']}%"
    plt.title(label)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return {"status": "ok", "image": image_base64}
