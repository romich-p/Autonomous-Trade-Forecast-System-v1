import os
import json

DB_PATH = os.environ.get("DB_PATH", "db.json")

# Убедимся, что путь существует
if os.path.dirname(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def load_database():
    if not os.path.exists(DB_PATH):
        print("[DB] db.json не найден, создаём новый файл")
        return {}
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[DB] Ошибка загрузки базы: {e}")
        return {}

def save_database(db):
    try:
        with open(DB_PATH, "w") as f:
            json.dump(db, f)
    except Exception as e:
        print(f"[DB] Ошибка сохранения базы: {e}")
