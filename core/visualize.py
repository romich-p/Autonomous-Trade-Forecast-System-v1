import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from analyzer import analyze_candles


def visualize_plot(ticker, timeframe, candles, signals, advanced_signals):
    if not candles:
        return None

    fig, ax = plt.subplots(figsize=(12, 6))

    times = [datetime.fromtimestamp(c["time"]) for c in candles]
    closes = [c["close"] for c in candles]

    ax.plot(times, closes, label="Close", linewidth=1.5)

    for signal in signals:
        t = datetime.fromtimestamp(signal["time"])
        if signal["type"] == "sma_crossover":
            ax.axvline(t, color="blue", linestyle="--", alpha=0.4)
            ax.text(t, max(closes), "SMA", rotation=90, color="blue", fontsize=8, ha='right')
        elif signal["type"] == "tp_sl":
            label = f"T.{signal['side'].upper()}" if signal.get("side") != "flat" else "EXIT"
            ax.axvline(t, color="green" if signal["side"] == "long" else "red", linestyle=":", alpha=0.6)
            ax.text(t, min(closes), label, rotation=90, color="green" if signal["side"] == "long" else "red",
                    fontsize=8, ha='left')

    analysis = analyze_candles(ticker, timeframe, candles, signals, advanced_signals)
    summary = (
        f"Trend: {analysis['trend']} ({analysis['trend_strength']}%)\n"
        f"Optimality: {analysis['entry_optimality']}%\n"
        f"Side: {analysis['entry_side']}"
    )
    ax.set_title(f"{ticker} {timeframe}\n{summary}")
    ax.legend()
    ax.grid(True)

    # Преобразование в base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64
