def analyze_candles(ticker, timeframe, candles, signals, advanced_signals):
    if not candles:
        return {
            "trend": "unknown",
            "trend_strength": 0,
            "entry_optimality": 0,
            "entry_side": "none"
        }

    last_candle = candles[-1]

    # Простой анализ тренда по закрытию
    closes = [c["close"] for c in candles[-5:]]
    if all(earlier < later for earlier, later in zip(closes, closes[1:])):
        trend = "up"
        strength = 100
    elif all(earlier > later for earlier, later in zip(closes, closes[1:])):
        trend = "down"
        strength = 100
    else:
        trend = "flat"
        strength = 30

    # Оптимальность входа — если последняя свеча против тренда (откат) — даём высокий балл
    if trend == "up" and last_candle["close"] < last_candle["open"]:
        entry_optimality = 80
    elif trend == "down" and last_candle["close"] > last_candle["open"]:
        entry_optimality = 80
    else:
        entry_optimality = 40

    entry_side = "with trend" if entry_optimality > 50 else "against trend"

    return {
        "trend": trend,
        "trend_strength": strength,
        "entry_optimality": entry_optimality,
        "entry_side": entry_side
    }
