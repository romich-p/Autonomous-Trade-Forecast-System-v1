import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from flask import Response
import io
from .data_store import candles, signals, advanced_signals

def plot_chart(ticker: str, timeframe: str):
    df = candles.get((ticker, timeframe), [])
    if not df:
        return f"No data for {ticker} {timeframe}"

    # Преобразуем в DataFrame
    df = pd.DataFrame(df)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Отображаем свечи
    for idx, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([idx, idx], [row['low'], row['high']], color='black')  # тень
        ax.plot([idx, idx], [row['open'], row['close']], color=color, linewidth=4)  # тело

    # Добавим сигналы
    sigs = signals.get((ticker, timeframe), [])
    for s in sigs:
        t = pd.to_datetime(s["time"])
        label = s["action"]
        color = "blue" if label == "buy" else "orange"
        ax.axvline(t, color=color, linestyle="--", alpha=0.5)
        ax.text(t, ax.get_ylim()[1], label.upper(), rotation=90, color=color, verticalalignment='top')

    # Advanced сигналы
    adv = advanced_signals.get((ticker, timeframe), [])
    for s in adv:
        t = pd.to_datetime(s["time"])
        if s["action"] == "tp_sl":
            side = s.get("side", "flat")
            label = f"TP/SL: {side}"
            ax.axvline(t, color="purple", linestyle=":", alpha=0.5)
            ax.text(t, ax.get_ylim()[0], label, rotation=90, color="purple", verticalalignment='bottom')

    ax.set_title(f"{ticker} {timeframe} Chart")
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Конвертация в PNG
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return Response(buf.getvalue(), mimetype='image/png')
