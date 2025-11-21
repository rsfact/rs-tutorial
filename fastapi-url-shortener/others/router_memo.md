```python
def shorten_url(
    data: schemas.ShortenRequest = Body(...),
    db: Session = Depends(get_db)
):
```
## data
HTTPリクエストのbody(JSON)を受け取る引数の名前
## = Body(...)
FastAPIに「これはJSONボディとして受け取りなさい」って指示してる
💡 つまり：
✨ 「POST の JSON を ‘data’ という名前で受け取る」
✨ 「JSON は必ず ShortenRequest の形で来なきゃダメ」
✨ 「JSON が無いとエラー」
って意味！
req: Schema(stock-managerのshemas_app)だけだと、FastAPIはBodyと推測（Queryと誤解されることも！？）
req: Schema = Body(...) これだと確定でJSON Bodyになる
必ずbodyとして扱われるように書いておく

## db: Session = Depends(get_db)
これはFastAPIの依存型注入。この関数の中で使う DB 接続をここに入れる。変数名 db は好きに決められる（一般的には db）
## db
この関数内でつかうDBセッション(SQLAlchemyのやつ)
## Session
型ヒント(SQLAlchemyのSession)
## = Depends(get_db)
FastAPI に：✨「この関数を呼ぶとき、get_db() を実行して、その戻り値を db に入れてね」とお願いしている。

💡 get_db() の動き
db.py にこうあったよね？
  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()
FastAPI は関数が呼ばれるたびに SessionLocal() を自動で作って → 渡して → 終わったら閉じるところまでやってくれる！


db: Session と db = SessionLocal() は同じものなの？
→ うん！！同じ db のこと！！

FastAPI の仕組みでこうなる：
router が呼ばれる
FastAPI が get_db() を呼ぶ
SessionLocal() が作られる
できた db が router に注入される
だから router では
  db.query(...)
  db.add(...)
  db.commit()
が使えるようになる。


# if cruds.find_by_from_name(db, data.from_name):
✨(1) db — SQLAlchemy の DB セッション
✔ これは router の引数で受け取っていたやつ
  db: Session = Depends(get_db)
  FastAPI が自動で
  「データベースにつながった SessionLocal()」 を作ってくれて、
  それが db という変数に入ってる。
✔ cruds では db をこう使う
  db.query(Url).filter(...).first()
  だから cruds に渡さないと DB にアクセスできない。
✨(2) data.from_name — ユーザーの JSON の値
リクエストボディがこう来るでしょ？
{
  "from_name": "kanoko",
  "to_url": "https://google.com"
}
これを router が受け取ると：
data.from_name  # "kanoko"
data.to_url     # "https://google.com"
となる。
✔ data は ShortenRequest のインスタンス
例：
data = ShortenRequest(from_name="kanoko", to_url="https://google.com")
だからこう取り出す。

# return result
crudsでdb.refresh(url)するとurl の中身はこうなる👇
Url(
  id=1,
  from_name="abc",
  to_url="https://...",
  count=0,
  created_at="2025-01-01T12:34:56"
)
だからreturn urlはid, from_name, to_url, count, created_at すべてを含むモデルオブジェクト。
最終的にresponsemodel指定されているのでShortenResponseの形に整形してJSONで返してくれる。


# RedirectResponse
⭐ RedirectResponse は何者？
✔ FastAPI が提供するレスポンスクラス
✔ HTTPステータス 302（移動）を返す
✔ ブラウザに「こっちへ移動して」と指示する
✔ url= に指定した先へ勝手に移動する

普通の JSON を返すレスポンスとは違う、特別なレスポンスなの！