# FastAPIによる短縮URLサービス

## 概要

このプロジェクトでは、FastAPIを使用して簡単なURL短縮サービスを作成します。このサービスでは、長いURLを短いURLに変換し、短いURLにアクセスすると元のURLにリダイレクトされます。

## 機能要件

1. ユーザーが元のURL (長いURL) と短縮名を指定して、短縮URLを作成できる
2. 短縮URLにアクセスすると、元のURLにリダイレクトされる
3. 短縮URLにアクセスされた回数を記録する
4. データはSQlite（`db.sqlite`）に保存される


## 技術仕様

- フレームワーク: FastAPI
- データベース: SQLite

テーブル名: urls
| カラム名      | 型         | 説明                        |
|:------------|:----------|:--------------------------|
| id          | TEXT      | 一意のUUID主キー              |
| from_name   | TEXT      | ユーザーが指定する短縮名（ユニーク）|
| to_url      | TEXT      | 元の長いURL                  |
| count       | INTEGER   | リダイレクト回数（デフォルト0）   |
| created_at  | TIMESTAMP | レコード作成日時               |


## 環境構築

```bash
python -m venv .venv
source .venv/Scripts/activate # Windows
source .venv/bin/activate # Mac
pip install -r requirements.txt
```

```bash
cd database
touch db.sqlite
python initialize.py
# カラムが作られているのを確認しましょう
```

## 実装手順

### STEP1: FastAPIを立ててみよう

`Hello World`が返るような、最も基本的なエンドポイント``GET：localhost:8000/`を作成し、動作を確認する。

```bash
# サーバーを起動する
cd backend
python main.py
```
[Swagger UI](http://localhost:8000/docs)にアクセスする。


### STEP2: API通信の型=スキーマの定義

1. リクエストモデル (`ReqShorten`) を作成する
   - `from_name`: 短縮URLの名前部分
   - `to_url`: リダイレクト先の元URL
2. レスポンスモデル (`ResShorten`) を作成する
   - `id`: 一意のUUID
   - `from_name`: 短縮URLの名前
   - `to_url`: リダイレクト先の元URL
   - `count`: 転送回数

### STEP3: データベース操作関数の実装

1. `db.sqlite`にデータを保存する関数を作成する
2. `db.sqlite`からデータを読み込む関数を作成する
3. `db.sqlite`が存在しない場合は新しく作成する処理を追加する

### STEP4: APIエンドポイントの実装

1. URL短縮エンドポイント (`POST：localhost:8000/shorten`) を作成する
   - POSTリクエストを受け付ける
   - 短縮名の重複チェックを行う
   - 新しい短縮URLを作成してデータベースに保存する
   - 作成した短縮URLの情報を返す (上記のレスポンスモデルを参照)
2. リダイレクトエンドポイント (`GET：localhost:8000/u/{name}`) を作成する
   - GETリクエストを受け付ける
   - 指定された名前に対応するURLを検索する
   - アクセス回数をカウントアップする
   - 元のURLにリダイレクトする（`Pydantic`の`RedirectResponse`を使用します）
   - URLが見つからない場合は404エラーを返す

### STEP5: テスト

1. サーバーを起動し、Swagger UIにアクセスする
2. `/shorten`エンドポイントを使って短縮URLを作成する

     ```json
     {
       "from_name": "google",
       "to_url": "https://www.google.com"
     }
     ```

3. 作成された短縮URL (例: `http://localhost:8000/u/google`) にアクセスして、リダイレクトされることを確認する

### STEP6: 一般公開する

- ngrokを用いて公開URLを発行する。
- リンクを開いたら、自身のLINE登録URLに転送させるようにしてみてください。
- 例: `https://example.ngrok-free.app/u/line` -> `https://line.me/R/ti/p/@1234567890`


### STEP7: リダイレクトURLの発行をするフロントエンドを簡易的に実装する
from_nameとto_urlをインプットとして、リダイレクトURLを返す最も簡単なフロントを実装しよう。目指せ100行以内。

```bash
mkdir frontend
cd frontend
touch index.html
# コードを書いてください。
```

```bash
python -m http.server 8001
open http://localhost:8001
```
