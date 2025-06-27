import os
import matplotlib.pyplot as plt
import pandas as pd

from core.data_store import candles
from core.analyze_plotter import analyze_trend_and_entry

def plot_chart(ticker: str, timeframe: str):
    key = f"{ticker}_{timeframe}"
    df = candles.get(key, [])
    if not df or len(df) < 2:
        return None

    df = pd.DataFrame(df)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    # Анализ
    analysis = analyze_trend_and_entry(ticker, timeframe)
    trend_str = f"Trend: {analysis['trend_direction']} ({analysis['trend_strength']})" if analysis else ""
    entry_str = f"Entry: {analysis['entry_side']} ({analysis['entry_optimality']}%)" if analysis and analysis["entry_optimality"] is not None else ""

    # Построение графика
    fig, ax = plt.subplots(figsize=(10, 4))
    df["close"].plot(ax=ax, label="Close", linewidth=1)

    if "ma_fast" in df.columns:
        df["ma_fast"].plot(ax=ax, label="MA Fast", linestyle="--")
    if "ma_slow" in df.columns:
        df["ma_slow"].plot(ax=ax, label="MA Slow", linestyle="--")

    ax.set_title(f"{ticker} {timeframe}\n{trend_str} | {entry_str}")
    ax.legend()
    ax.grid(True)

    # Сохранение
    os.makedirs("static", exist_ok=True)
    image_path = f"static/{ticker}_{timeframe}.png"
    plt.savefig(image_path)
    plt.close()

    return image_path
