```python
def find_by_from_name(db: Session, from_name: str):
    return db.query(Url).filter(Url.from_name == from_name).first()
```
🌟db: Session は CRUD の関数に毎回書く“おまじない” と思っていい！
今の段階では 深く理解してなくてもいいやつ！
FastAPI ＋ SQLAlchemy を使うときは、
def なんとか(db: Session, 他の引数...):
と書くのが“お作法”なんだよ💛

## db.query(url)
「Urlテーブル(urlsテーブル)を使うよ」という宣言。SQLにすると： FROM urls
## .filter(Url.from_name == from_name)
WHERE条件。SQLにすると: WHERE from_name = ?
## .first()
「結果の最初の1件だけ返してね」という意味。SQLにすると: LIMIT 1
これをつけないと
  result = db.query(Url).filter(Url.from_name == from_name)
これだと返ってくるのはQuery(クエリオブジェクト)であって「実際のデータ」ではない。つまりまだSQLが実行されてない状態。
.first()をつけてやっとSQLを実行して結果を実際のデータとして1件だけ返してくれる。
- .first() → SELECT して1件だけオブジェクトを返す
- .one() → 1件のみ存在する前提（0件や2件では例外）
- .all() → 全件リストで返す
今回の用途では .first() が最適❣️
✔ .one()（厳密）
結果が ちょうど1件 のとき → OK
結果が 0件 のとき → エラーになる（NoResultFound）
結果が 2件以上 → エラーになる（MultipleResultsFound）
→ アプリが落ちる可能性がある
✔ .first()（ゆるい・安全）
1件ある → その1件が返る
0件 → None が返る（エラーにならない）
2件以上 → 最初の1件が返る（unique なら起きない）
→ エラーにならない


# url = Url()...
```python
url = Url(
    from_name=from_name,
    to_url=to_url,
)
```
これだけで
INSERT INTO urls (from_name, to_url, count, created_at) VALUES (?, ?, ?, ?)
の準備が整う。created_atやcountはmodels側でdefault設定してるから不要
## db.add(url)
「このレコードを追加してね」とSQLAlchemyに教える。
## db.commit()
ここで初めてINSERTが実行される。
1️⃣ 新しいレコードを DB に INSERT
2️⃣ default の値（count=0, created_at=現在時刻）を設定
3️⃣ id を自動採番（AUTOINCREMENT）
でもこの時点では Python側の url には反映されていない。
## db.refresh(url)
commitの直後、idやcreated_atのような自動生成された値を、Pythonのオブジェクトに反映してくれる超大事な処理。これがないとurl.idがNoneのままになる。
「今 DB に保存された最新の値を読み直して、url オブジェクトに反映してね！」
refresh のあと、url の中身はこうなる👇
Url(
  id=1,
  from_name="abc",
  to_url="https://...",
  count=0,
  created_at="2025-01-01T12:34:56"
)
🌟countやcreated_atも入るのがポイント！
## return url
返すのはdictじゃなくてモデルのインスタンス。
FastAPIはpydanticのschemaで自動的にJSONに変換してくれる（CRUDからrouterに返したあとの話）。
CRUDがUrlインスタンスをretrunした段階ではJSONではない。Pythonのオブジェクト(SQLAlchemyのモデル)のまま

# def increment_count_and_get_url()
from_name の短縮URLがDBに存在するか探す
存在しない → None を返す（リダイレクトできない）
存在する → count を +1 する
と同時に to_url を返す（リダイレクトできる）