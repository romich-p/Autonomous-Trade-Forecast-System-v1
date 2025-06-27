from core.analyzer import analyze_market

def analyze_trend_and_entry(ticker: str, timeframe: str):
    try:
        result = analyze_market(ticker, timeframe)
        return result or {
            "trend_direction": "unknown",
            "trend_strength": 0,
            "entry_optimality": None,
            "entry_side": None
        }
    except Exception as e:
        return {
            "trend_direction": "error",
            "trend_strength": 0,
            "entry_optimality": None,
            "entry_side": None
        }
