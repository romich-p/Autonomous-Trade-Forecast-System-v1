import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from flask import Response
import io
from .data_store import candles, signals, advanced_signals
from .analyze_plotter import analyze_trend_and_entry

DISABLED_TIMEFRAMES = {"5S", "45S", "10M"}

def plot_chart(ticker: str, timeframe: str):
    if timeframe.upper() in DISABLED_TIMEFRAMES:
        return f"Timeframe {timeframe} is disabled"

    key = f"{ticker}_{timeframe}"
    df = candles.get(key, [])
    if not df:
        return f"No data for {ticker} {timeframe}"

    df = pd.DataFrame(df)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    fig, ax = plt.subplots(figsize=(12, 6))

    for idx, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([idx, idx], [row['low'], row['high']], color='black')
        ax.plot([idx, idx], [row['open'], row['close']], color=color, linewidth=4)

    for s in signals.get(key, []):
        t = pd.to_datetime(s["time"])
        label = s["action"]
        color = "blue" if label == "buy" else "orange"
        ax.axvline(t, color=color, linestyle="--", alpha=0.5)
        ax.text(t, ax.get_ylim()[1], label.upper(), rotation=90, color=color, verticalalignment='top')

    for s in advanced_signals.get(key, []):
        t = pd.to_datetime(s["time"])
        if s["action"] == "tp_sl":
            side = s.get("side", "flat")
            if side == "long":
                label = "T.LONG"
            elif side == "short":
                label = "T.SHORT"
            else:
                label = "TP/SL: flat"
            ax.axvline(t, color="purple", linestyle=":", alpha=0.5)
            ax.text(t, ax.get_ylim()[0], label, rotation=90, color="purple", verticalalignment='bottom')

    summary = analyze_trend_and_entry(df, advanced_signals.get(key, []))
    if summary:
        ax.text(0.01, 0.95, summary, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.6))

    ax.set_title(f"{ticker} {timeframe} Chart")
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return Response(buf.getvalue(), mimetype='image/png')
