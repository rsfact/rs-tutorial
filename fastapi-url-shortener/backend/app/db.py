import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "database" / "db.json"


def save_db(data):
    """
    データをファイルに保存する。
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_db():
    """
    データベースファイルを読み込む。
    """
    # ファイルが存在しなければ作成する
    if not os.path.exists(DB_FILE):
        save_db([])
        return []

    # ファイルが存在したら中身を返す
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)