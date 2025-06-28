import matplotlib.pyplot as plt
import io
from analyzer import analyze_candles

def visualize_plot(ticker, timeframe, candles, signals, advanced_signals):
    fig, ax = plt.subplots(figsize=(12, 6))
    if not candles:
        return None

    times = [c['time'] for c in candles]
    prices = [c['close'] for c in candles]
    ax.plot(times, prices, label=f"{ticker} {timeframe}")

    for sig in signals:
        ax.scatter(sig['time'], sig['price'], marker='o', color='green' if sig['side'] == 'long' else 'red')

    for adv in advanced_signals:
        ax.scatter(adv['time'], adv['price'], marker='x', color='blue')

    ax.legend()
    ax.set_title(f"{ticker} {timeframe} Chart")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf
