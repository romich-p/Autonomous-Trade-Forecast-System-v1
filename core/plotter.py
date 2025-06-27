import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from flask import Response
import io
from .data_store import candles, signals, advanced_signals
from .analyzer import analyze_market  # ✅ заменили импорт

def plot_chart(ticker: str, timeframe: str):
    key = f"{ticker}_{timeframe}"
    raw = candles.get(key, [])

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

    for idx, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([idx, idx], [row['low'], row['high']], color='black')
        ax.plot([idx, idx], [row['open'], row['close']], color=color, linewidth=4)

    sigs = signals.get(key, [])
    for s in sigs:
        t = pd.to_datetime(s["time"], errors="coerce")
        if pd.isna(t): continue
        label = s["action"]
        color = "blue" if label == "buy" else "orange"
        ax.axvline(t, color=color, linestyle="--", alpha=0.5)
        ax.text(t, ax.get_ylim()[1], label.upper(), rotation=90, color=color, verticalalignment='top')

    adv = advanced_signals.get(key, [])
    for s in adv:
        t = pd.to_datetime(s["time"], errors="coerce")
        if pd.isna(t): continue
        if s["action"] == "tp_sl":
            side = s.get("side", "flat")
            label = "T.LONG" if side == "long" else "T.SHORT" if side == "short" else "TP/SL: flat"
            ax.axvline(t, color="purple", linestyle=":", alpha=0.5)
            ax.text(t, ax.get_ylim()[0], label, rotation=90, color="purple", verticalalignment='bottom')

    # ✅ Используем правильную функцию анализа
    analysis = analyze_market(ticker, timeframe)
    if analysis:
        text = (
            f"Trend: {analysis['trend_direction']}\n"
            f"Strength: {analysis['trend_strength']}\n"
            f"Entry: {analysis['entry_side']} ({analysis['entry_optimality']}%)"
        )
        ax.text(
            1.01, 0.99, text,
            transform=ax.transAxes,
            verticalalignment='top',
            fontsize=10,
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5')
        )

    ax.set_title(f"{ticker} {timeframe} Chart")
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return Response(buf.getvalue(), mimetype='image/png')
