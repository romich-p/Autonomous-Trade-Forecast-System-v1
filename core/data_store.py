import datetime

# === Хранилище данных ===
candles = {}  # Формат: {'GBPUSD_15S': [ {candle}, ... ]}
signals = []  # Простые сигналы (от crossover стратегии)
advanced_signals = []  # Сигналы от технической стратегии

# === Функция: Сохраняем свечу ===
def store_candle(data):
    key = f"{data['ticker']}_{data['timeframe']}"
    if key not in candles:
        candles[key] = []

    # Проверка на дубликаты по времени
    if any(c['time'] == data['time'] for c in candles[key]):
        return

    # Добавляем новую свечу
    candles[key].append({
        "time": data["time"],
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data.get("volume", 0))
    })

    # Сортировка по времени
    candles[key].sort(key=lambda x: x["time"])

# === Функция: Получить последние N свечей ===
def get_recent_candles(ticker_tf, n=100):
    return candles.get(ticker_tf, [])[-n:]

# === Функция: Сохраняем сигнал ===
def store_signal(data, advanced=False):
    target = advanced_signals if advanced else signals

    signal_data = {
        "ticker": data["ticker"],
        "timeframe": data["timeframe"],
        "time": data.get("time", datetime.datetime.utcnow().isoformat())
    }

    if advanced:
        signal_data["action"] = data["action"]
        signal_data["sltp"] = float(data.get("sltp", 0))
        signal_data["side"] = data.get("side", "flat")
    else:
        signal_data["action"] = data["action"]
        signal_data["contracts"] = float(data.get("contracts", 0))
        signal_data["position_size"] = float(data.get("position_size", 0))

    target.append(signal_data)
