from fastapi import FastAPI

app = FastAPI(
    title="URL Shortener",
    description="URL shortener service",
    version="0.1.0"
    docs_url="/api/docs",
)

# データベース接続設定をここに

# スキーマをここに

# 各種エンドポイントをここに

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
