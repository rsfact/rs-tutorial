from fastapi import FastAPI, Body
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from pydantic import BaseModel, Field
import sqlite3

# 定数
DB_FILE = "db.sqlite"


# データベース操作関数
def get_db():
    """
    データベースを取得する。
    """
    return sqlite3.connect(DB_FILE)


# スキーマ
class ShortenRequest(BaseModel):
    """
    リクエスト: URL登録
    """
    from_name: str = Field(..., example="redirect")
    to_url: str = Field(..., example="https://www.premierleague.com/en")


class ShortenResponse(BaseModel):
    """
    レスポンス: URL登録
    """
    id: str
    from_name: str
    to_url: str
    count: int


# APIサーバ設定
app = FastAPI(
    title="URL Shortener",
    description="My URL shortener",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 各種エンドポイント

@app.get("/")
def hello():
    """
    ルートエンドポイント
    """
    return {"msg": "Hello, World!"}


@app.post("/shorten")
def shorten_url(data: ShortenRequest = Body(...)):
    """
    URLを短縮する。
    """
    from_name = data.from_name
    to_url = data.to_url

    if not from_name or not to_url:
        return JSONResponse(status_code=400, content={"error": "from_nameとto_urlは必須です"})

    # データベースの読み込み
    db = get_db()

    # from_name の重複チェック
    cursor = db.execute("SELECT * FROM urls WHERE from_name = ?", (from_name,))
    if cursor.fetchone():
        return JSONResponse(status_code=409, content={"error": "from_nameは既に使用されています"})

    # 新しい項目の作成
    uid = str(uuid.uuid4())

    # 新しい項目をデータベースに追加
    db.execute("INSERT INTO urls (id, from_name, to_url, count) VALUES (?, ?, ?, ?)", (uid, from_name, to_url, 0))
    db.commit()

    # データベースの保存
    db.close()

    # レスポンスの作成
    return {
        "id": uid,
        "from_name": from_name,
        "to_url": to_url,
        "count": 0
    }


@app.get("/u/{name}")
def redirect(name):
    """
    短縮URLから元のURLにリダイレクトする。
    """
    db = get_db()

    # 該当するエントリを検索
    cursor = db.execute("SELECT * FROM urls WHERE from_name = ?", (name,))
    item = cursor.fetchone()
    if item:
        # 転送回数を加算して記録
        db.execute("UPDATE urls SET count = count + 1 WHERE id = ?", (item[0],))
        db.commit()
        return RedirectResponse(url=item[2])
    db.close()
    return JSONResponse(status_code=404, content={"error": "URLが見つかりません"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
