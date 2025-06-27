# core/plotter.py
import plotly.graph_objects as go
from core.data_store import candles, signals, advanced_signals
from datetime import datetime

def plot_chart(ticker: str, timeframe: str, limit: int = 100):
    key = (ticker, timeframe)
    if key not in candles:
        return f"No candles for {ticker} {timeframe}"

    data = candles[key][-limit:]
    df = [c for c in data if all(k in c for k in ["time", "open", "high", "low", "close"])]

    if not df:
        return f"Not enough candle data to plot"

    times = [datetime.fromisoformat(c["time"].replace("Z", "+00:00")) for c in df]
    open_prices = [c["open"] for c in df]
    high_prices = [c["high"] for c in df]
    low_prices = [c["low"] for c in df]
    close_prices = [c["close"] for c in df]

    fig = go.Figure(data=[
        go.Candlestick(
            x=times,
            open=open_prices,
            high=high_prices,
            low=low_prices,
            close=close_prices,
            name="Candles"
        )
    ])

    # Overlay crossover signals
    for sig in signals.get(key, []):
        t = datetime.fromisoformat(sig["time"].replace("Z", "+00:00"))
        color = "green" if sig["action"] == "buy" else "red"
        fig.add_trace(go.Scatter(
            x=[t], y=[sig["price"]],
            mode="markers",
            marker=dict(color=color, size=10),
            name=f"Cross {sig['action']}"
        ))

    # Overlay technical rating TP/SL signals
    for s in advanced_signals.get(key, []):
        t = datetime.fromisoformat(s["time"].replace("Z", "+00:00"))
        price = s.get("price", None)
        if not price:
            continue
        if s["action"] == "tp_sl":
            color = "gray"
        elif s["action"] == "buy":
            color = "blue"
        elif s["action"] == "sell":
            color = "orange"
        else:
            continue

        fig.add_trace(go.Scatter(
            x=[t], y=[price],
            mode="markers",
            marker=dict(color=color, size=8, symbol="x"),
            name=f"{s['action']} ({s['side']})"
        ))

    fig.update_layout(title=f"{ticker} {timeframe} - Signals", xaxis_title="Time", yaxis_title="Price")
    return fig.to_html()
<вставим позже>