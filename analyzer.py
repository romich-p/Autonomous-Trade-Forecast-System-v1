import pandas as pd
from core.data_store import candles, signals, advanced_signals

def analyze_market(ticker: str, timeframe: str):
    key = f"{ticker}_{timeframe}"
    df = candles.get(key, [])
    if not df or len(df) < 20:
        return None

    df = pd.DataFrame(df)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    df["ma_fast"] = df["close"].rolling(5).mean()
    df["ma_slow"] = df["close"].rolling(15).mean()

    trend_direction = "up" if df["ma_fast"].iloc[-1] > df["ma_slow"].iloc[-1] else "down"
    trend_strength = abs(df["ma_fast"].iloc[-1] - df["ma_slow"].iloc[-1])

    last_signal = next((s for s in reversed(signals.get((ticker, timeframe), [])) if s["time"] in df.index), None)
    last_adv_signal = next((s for s in reversed(advanced_signals.get((ticker, timeframe), [])) if s["time"] in df.index), None)

    entry_optimality = None
    side = None
    if last_signal:
        sig_dir = last_signal["action"]
        side = "with trend" if (sig_dir == "buy" and trend_direction == "up") or (sig_dir == "sell" and trend_direction == "down") else "against trend"
        entry_optimality = 100 if side == "with trend" else 40
    elif last_adv_signal:
        side_value = last_adv_signal.get("side")
        if side_value in ["long", "short"]:
            sig_dir = "buy" if side_value == "long" else "sell"
            side = "with trend" if (sig_dir == "buy" and trend_direction == "up") or (sig_dir == "sell" and trend_direction == "down") else "against trend"
            entry_optimality = 90 if side == "with trend" else 50

    return {
        "trend_direction": trend_direction,
        "trend_strength": round(trend_strength, 5),
        "entry_optimality": entry_optimality,
        "entry_side": side
    }
