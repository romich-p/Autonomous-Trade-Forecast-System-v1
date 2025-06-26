from core.data_store import get_recent_candles, signals
from core.bos_detector import detect_structure

def body_strength(candle):
    body = abs(candle["close"] - candle["open"])
    range_ = candle["high"] - candle["low"]
    return body / range_ if range_ > 0 else 0

def make_prediction(data):
    ticker = data["ticker"]
    tf = data["timeframe"]

    candles = get_recent_candles(ticker, tf)
    if not candles or len(candles) < 10:
        return {
            "trend": "unknown",
            "structure_broken": False,
            "continuation_probability": 0.0,
            "entry_score": 0.0,
            "direction": None,
            "reason": "Not enough candles"
        }

    structure = detect_structure(candles)
    trend = structure["trend"]
    structure_broken = structure["structure_broken"]
    bos_direction = structure["bos_direction"]

    last_candle = candles[-1]
    second_last = candles[-2]
    body_power = body_strength(last_candle)

    entry_direction = trend
    if structure_broken:
        entry_direction = "long" if bos_direction == "up" else "short"

    continuation_probability = 60.0
    entry_score = 65.0
    reason = ""

    if structure_broken:
        if body_power > 0.6:
            continuation_probability += 15
            entry_score += 10
            reason = "Strong BOS breakout"
        elif body_power < 0.3:
            continuation_probability -= 10
            entry_score -= 10
            reason = "Weak BOS, low conviction"
        else:
            reason = "Neutral BOS"
    else:
        if trend == "up" and last_candle["low"] > second_last["low"]:
            continuation_probability += 10
            reason = "Pullback in uptrend"
        elif trend == "down" and last_candle["high"] < second_last["high"]:
            continuation_probability += 10
            reason = "Pullback in downtrend"
        else:
            reason = "Sideways movement"

    last_signal = signals.get(ticker, [])[-1] if signals.get(ticker) else None
    if last_signal and last_signal["timeframe"] == tf:
        if last_signal["action"] == "buy" and entry_direction == "long":
            continuation_probability += 10
            entry_score += 10
            reason += " + Signal agrees"
        elif last_signal["action"] == "sell" and entry_direction == "short":
            continuation_probability += 10
            entry_score += 10
            reason += " + Signal agrees"
        else:
            entry_score -= 10
            reason += " + Signal disagrees"

    continuation_probability = round(min(max(continuation_probability, 0), 100), 2)
    entry_score = round(min(max(entry_score, 0), 100), 2)

    return {
        "trend": trend,
        "structure_broken": structure_broken,
        "bos_direction": bos_direction,
        "continuation_probability": continuation_probability,
        "entry_score": entry_score,
        "direction": entry_direction,
        "reason": reason
    }