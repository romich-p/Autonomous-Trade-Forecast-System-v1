def analyze_trend_and_entry(df, adv_signals):
    if df is None or len(df) < 20:
        return ""

    df["ma_fast"] = df["close"].rolling(5).mean()
    df["ma_slow"] = df["close"].rolling(15).mean()

    trend_direction = "up" if df["ma_fast"].iloc[-1] > df["ma_slow"].iloc[-1] else "down"
    trend_strength = round(abs(df["ma_fast"].iloc[-1] - df["ma_slow"].iloc[-1]), 5)

    last_adv = next((s for s in reversed(adv_signals) if s["action"] == "tp_sl" and s.get("side") in ["long", "short"]), None)
    if last_adv:
        side = last_adv["side"]
        sig_dir = "buy" if side == "long" else "sell"
        alignment = "with trend" if (sig_dir == "buy" and trend_direction == "up") or (sig_dir == "sell" and trend_direction == "down") else "against trend"
        entry_opt = 90 if alignment == "with trend" else 50
    else:
        alignment = "n/a"
        entry_opt = "n/a"

    return (
        f"Trend: {trend_direction}\n"
        f"Strength: {trend_strength}\n"
        f"Entry: {alignment} ({entry_opt}%)"
    )
