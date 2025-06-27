# core/dump_utils.py
from core.data_store import candles, signals, advanced_signals

def export_data_to_py():
    with open("core/db_export.py", "w") as f:
        f.write("# Автогенерируемый файл. Не редактируй вручную.\n\n")
        f.write(f"candles_data = {repr(candles)}\n")
        f.write(f"signals_data = {repr(signals)}\n")
        f.write(f"advanced_signals_data = {repr(advanced_signals)}\n")
