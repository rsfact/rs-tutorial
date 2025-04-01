# FastAPIによる自作短縮URLサービス

## 課題内容

### 概要

このプロジェクトでは、FastAPIを使用して簡単なURL短縮サービスを作成します。このサービスでは、長いURLを短いURLに変換し、短いURLにアクセスすると元のURLにリダイレクトされます。

### 機能要件

1. ユーザーが元のURL (長いURL) と短縮名を指定して、短縮URLを作成できる
2. 短縮URLにアクセスすると、元のURLにリダイレクトされる
3. 短縮URLがアクセスされた回数を記録する
4. データはJSONファイルに保存される

### 技術仕様

- フレームワーク: FastAPI
- データ保存: JSONファイル

### ディレクトリ構造

```bash
/
├── main.py
├── requirements.txt
└── db.json
```

### 実装手順

#### ステップ1: FastAPI設定

`GET /`で`Hello World`が返るような、最も基本的なエンドポイントを作成し、動作を確認する。

#### ステップ2: データモデルの定義

1. リクエストモデル (`ShortenRequest`) を作成する
   - `from_name`: 短縮URLの名前部分
   - `to_url`: リダイレクト先の元URL
2. レスポンスモデル (`ShortenResponse`) を作成する
   - `uuid`: 一意のID
   - `from_name`: 短縮URLの名前
   - `to_url`: リダイレクト先の元URL
   - `count`: 転送回数

#### ステップ3: データベース操作関数の実装

1. JSONファイルにデータを保存する関数を作成する
2. JSONファイルからデータを読み込む関数を作成する
3. ファイルが存在しない場合は新しく作成する処理を追加する

#### ステップ4: APIエンドポイントの実装

1. URL短縮エンドポイント (`/shorten`) を作成する
   - JSONのPOSTリクエストを受け付ける
   - 短縮名の重複チェックを行う
   - 新しい短縮URLを作成してデータベースに保存する
   - 作成した短縮URLの情報を返す (上記のレスポンスモデルを参照)
2. リダイレクトエンドポイント (`/u/{name}`) を作成する
   - GETリクエストを受け付ける
   - 指定された名前に対応するURLを検索する
   - アクセス回数をカウントアップする
   - 元のURLにリダイレクトする
   - URLが見つからない場合は404エラーを返す

### ステップ5: テスト

1. サーバーを起動し、Swagger UIにアクセスする
2. `/shorten`エンドポイントを使って短縮URLを作成する

     ```json
     {
       "from_name": "google",
       "to_url": "https://www.google.com"
     }
     ```

3. 作成された短縮URL (例: `http://localhost:8000/u/google`) にアクセスして、リダイレクトされることを確認する

### ステップ6: 応用課題

- ngrokを用いて公開URLを発行する。
  - ngrokで固定ドメインを発行する。
  - `line`で自分のLINE登録URLに転送させるようにする。 (例: `https://example.ngrok-free.app/u/line`)
- Conoha VPSを用いて、Linux環境にデプロイする。
  - tmuxを用いて2セッション作成し、本プログラムとngrokをそれぞれ起動し、外部からのアクセスを確認する。

---

## 環境構築

### 仮想環境を使う場合

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

### 仮想環境を使わない場合

```bash
pip install -r requirements.txt
```

## 起動

```bash
python main.py
```

[Swagger UI](http://localhost:8000/docs)にアクセスする。
