from fastapi import FastAPI
import sqlite3

# 定数
DB_FILE = "db.sqlite"


# データベース操作関数
def get_db():
    """
    データベースを取得する。
    """
    return sqlite3.connect(DB_FILE)


# APIサーバ設定
app = FastAPI(
    title="URL Shortener",
    description="My URL shortener",
    version="0.1.0"
)

# 各種エンドポイントをここに

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
