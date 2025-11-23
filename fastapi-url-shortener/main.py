from fastapi import FastAPI

app = FastAPI(
    title="URL Shortener",
    description="My URL shortener",
    version="0.1.0"
)

# データベース関連をここに

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
