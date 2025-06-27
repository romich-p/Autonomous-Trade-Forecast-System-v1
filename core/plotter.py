import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from flask import Response
import io
from .data_store import candles, signals, advanced_signals
from .analyze_plotter import analyze_trend_and_entry


def plot_chart(ticker: str, timeframe: str):
    key = f"{ticker}_{timeframe}"
    df_data = candles.get(key, [])

    print(f"[PLOT] Candles for {key}: {len(df_data)} entries")  # Отладка

    if not df_data:
        print(f"[PLOT] No candles found for {key}")
        return Response("No candle data", status=404)

    df = pd.DataFrame(df_data)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    fig, ax = plt.subplots(figsize=(12, 6))

    for idx, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([idx, idx], [row['low'], row['high']], color='black')
        ax.plot([idx, idx], [row['open'], row['close']], color=color, linewidth=4)

    sigs = signals.get(key, [])
    for s in sigs:
        t = pd.to_datetime(s["time"])
        label = s["action"]
        color = "blue" if label == "buy" else "orange"
        ax.axvline(t, color=color, linestyle="--", alpha=0.5)
        ax.text(t, ax.get_ylim()[1], label.upper(), rotation=90, color=color, verticalalignment='top')

    adv = advanced_signals.get(key, [])
    for s in adv:
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

    # Добавляем анализ
    try:
        trend_summary = analyze_trend_and_entry(df, adv)
        ax.text(0.01, 0.95, trend_summary, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.6))
    except Exception as e:
        print(f"[PLOT] Analyze error: {e}")

    ax.set_title(f"{ticker} {timeframe} Chart")
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    print(f"[PLOT] Chart rendered for {key}")
    return Response(buf.getvalue(), mimetype='image/png')
