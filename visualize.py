import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
import base64

def visualize_plot(candles, signals, advanced):
    if not candles:
        return None

    # Преобразуем timestamp в datetime
    times = [datetime.fromtimestamp(c['timestamp']) for c in candles]
    prices = [c['close'] for c in candles]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, prices, label="Close Price", linewidth=1.5)

    # Отметки сигналов
    for s in signals:
        t = datetime.fromtimestamp(s['timestamp'])
        label = s.get('type', '').upper()
        color = 'green' if label == 'LONG' else 'red'
        ax.axvline(t, color=color, linestyle='--', alpha=0.6)
        ax.text(t, max(prices), label, rotation=90, verticalalignment='bottom', fontsize=8)

    # Advanced сигналы (например TP/SL)
    for a in advanced:
        t = datetime.fromtimestamp(a['timestamp'])
        side = a.get('side', '').lower()
        label = 'T.LONG' if side == 'long' else 'T.SHORT' if side == 'short' else 'T.FLAT'
        color = 'blue' if side == 'long' else 'orange' if side == 'short' else 'gray'
        ax.axvline(t, color=color, linestyle=':', alpha=0.5)
        ax.text(t, min(prices), label, rotation=90, verticalalignment='top', fontsize=7)

    ax.set_title("GBP/USD Candle Chart with Signals")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.legend()

    # Формат времени по оси X
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # Сохраняем в base64
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
