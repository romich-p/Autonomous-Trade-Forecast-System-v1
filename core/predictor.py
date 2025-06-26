from core.data_store import get_recent_candles

# Заглушка: простейший прогноз (временно)
def make_prediction(data):
    # Пример: вернём статический ответ (можно заменить на анализ BOS и статистики)
    return {
        "trend_continuation_probability": 50.0,  # %
        "entry_opportunity_score": 50.0          # %
    }
