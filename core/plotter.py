import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from flask import Response
import io
from .data_store import candles, signals, advanced_signals
from .analyze_plotter import analyze_trend_and_entry

def plot_chart(ticker: str, timeframe: str):
    key = f"{ticker}_{timeframe}"
    raw = candles.get(key, [])

    # Логирование для отладки
    print("🔍 Все ключи:", list(candles.keys()))
    print("🔍 Строим для ключа:", key)
    print("🔍 Количество свечей:", len(raw))

    if not raw:
        return f"No data for {ticker} {timeframe}"

    try:
        df = pd.DataFrame(raw)
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"])
        df.set_index("time", inplace=True)
    except Exception as e:
        return f"Ошибка при подготовке данных: {e}"

    fig, ax = plt.subplots(figsize=(12, 6))

    # Свечи
    for idx, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([idx, idx], [row['low'], row['high']], color='black')  # тени
        ax.plot([idx, idx], [row['open'], row['close']], color=color, linewidth=4)  # тело

    # Простые сигналы
    sigs = signals.get(key, [])
    for s in sigs:
        t = pd.to_datetime(s["time"], errors="coerce")
        if pd.isna(t): continue
        label = s["action"]
        color = "blue" if label == "buy" else "orange"
        ax.axvline(t, color=color, linestyle="--", alpha=0.5)
        ax.text(t, ax.get_ylim()[1], label.upper(), rotation=90, color=color, verticalalignment='top')

    # Расширенные сигналы
    adv = advanced_signals.get(key, [])
    for s in adv:
        t = pd.to_datetime(s["time"], errors="coerce")
        if pd.isna(t): continue
        if s["action"] == "tp_sl":
            side = s.get("side", "flat")
            label = "T.LONG" if side == "long" else "T.SHORT" if side == "short" else "TP/SL: flat"
            ax.axvline(t, color="purple", linestyle=":", alpha=0.5)
            ax.text(t, ax.get_ylim()[0], label, rotation=90, color="purple", verticalalignment='bottom')

    # Анализ тренда и входа
    trend_summary = analyze_trend_and_entry(df, adv)
    ax.text(0.01, 0.95, trend_summary, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.6))

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
