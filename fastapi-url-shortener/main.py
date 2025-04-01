from fastapi import FastAPI, Body
from fastapi.responses import RedirectResponse, JSONResponse
import uuid
from pydantic import BaseModel
import json
import os

# 定数
DB_FILE = "db.json"


# データベース操作関数
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


# スキーマ
class ShortenRequest(BaseModel):
    """
    リクエスト: URL登録
    """
    from_name: str
    to_url: str

class ShortenResponse(BaseModel):
    """
    レスポンス: URL登録
    """
    uuid: str
    from_name: str
    to_url: str
    count: int


# APIサーバ設定
app = FastAPI(
    title="URL Shortener",
    description="My URL shortener",
    version="0.1.0"
)

# 各種エンドポイント
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
    db = load_db()

    # from_name の重複チェック
    for item in db:
        if item.get("from_name") == from_name:
            return JSONResponse(status_code=409, content={"error": "from_nameは既に使用されています"})

    # 新しい項目の作成
    uid = str(uuid.uuid4())
    new_item = {
        "uuid": uid,
        "from_name": from_name,
        "to_url": to_url,
        "count": 0
    }

    # 新しい項目をデータベースに追加
    db.append(new_item)

    # データベースの保存
    save_db(db)

    # レスポンスの作成
    return {
        "uuid": uid,
        "from_name": from_name,
        "to_url": to_url,
        "count": 0
    }


@app.get("/u/{name}")
def redirect(name):
    """
    短縮URLから元のURLにリダイレクトする。
    """
    db = load_db()

    # 該当するエントリを検索
    i = 0
    for item in db:
        if item["from_name"] == name:
            # 転送回数を加算して記録
            db[i]["count"] += 1
            save_db(db)

            # 転送
            return RedirectResponse(url=item["to_url"])
        i += 1

    return JSONResponse(status_code=404, content={"error": "URLが見つかりません"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
