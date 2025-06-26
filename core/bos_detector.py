def detect_structure(candles, window=5):
    if len(candles) < window + 2:
        return {
            "trend": "unknown",
            "structure_broken": False,
            "bos_direction": None
        }

    highs = [c["high"] for c in candles[-(window+2):-1]]
    lows = [c["low"] for c in candles[-(window+2):-1]]
    last_candle = candles[-1]

    prev_high = max(highs)
    prev_low = min(lows)

    structure_broken = False
    bos_direction = None

    if last_candle["close"] > prev_high:
        structure_broken = True
        bos_direction = "up"
    elif last_candle["close"] < prev_low:
        structure_broken = True
        bos_direction = "down"

    # Определим тренд по последним телам свечей
    closes = [c["close"] for c in candles[-(window+1):]]
    opens = [c["open"] for c in candles[-(window+1):]]
    up_moves = sum([1 for o, c in zip(opens, closes) if c > o])
    down_moves = sum([1 for o, c in zip(opens, closes) if c < o])

    if up_moves > down_moves:
        trend = "up"
    elif down_moves > up_moves:
        trend = "down"
    else:
        trend = "sideways"

    return {
        "trend": trend,
        "structure_broken": structure_broken,
        "bos_direction": bos_direction
    }