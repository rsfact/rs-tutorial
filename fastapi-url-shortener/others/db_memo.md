```python
conn = sqlite3.connect(str(db_path.resolve()))
conn.row_factory = sqlite3.Row
return conn
```

🔷 結論：この3行は「DB に接続して、結果を辞書風に扱えるようにする」ためのもの

# sqlite3.connect(...)
👉 データベースファイルに接続する
sqlite3.connect() は「データベースへ接続して "コネクション" を作る」関数。
db_path.resolve() →ファイルの 絶対パス（C:\Users\xxx...）に変換
str() → 文字列にして connect に渡す
📌 結果
conn = データベースと通信できるオブジェクト
これを使って：SQL 文を実行する。SELECT してデータを読むINSERT / UPDATE するなど全部やる。

# conn.row_factory = sqlite3.Row
👉 SELECT の結果を辞書みたいに扱えるようにする設定
「この DB コネクションで SELECT の結果を返すときは、
普通の tuple ではなく、 sqlite3.Row を使って返してね」
ここが超大事.
.row_factoryはSQLiteのConnectionオブジェクトが持ってる設定項目の1つ。.row_factory は “SELECT の返り値の形を決める設定プロパティ”
```python
conn.row_factory = sqlite3.Row
```
これは「このコネクションで SELECT した結果の行をどういう型で返すか？」を設定するための 変数 に値を代入しているだけ。
.row_factoryにに入れてるのは関数そのもの。
sqlite3.Rowは特別なクラスで、SELECT結果を辞書みたいに扱える、row["name"]みたいにアクセスできる便利な変換機。



通常の sqlite3 はこうなる👇
  ```python
  cursor.execute("SELECT id, name FROM users")
  row = cursor.fetchone()

  row[0]  # id
  row[1]  # name
  ```
番号でしかアクセスできない。可読性が死ぬ。
🔥 でも row_factory を設定すると……
  ```python
  row = cursor.fetchone()

  row["id"]
  row["name"]
  ```
こうなる！！！
めっちゃ読みやすいし、ミスも減る💙





# from sqlalchemy import create_engine
データベースに接続するためのエンジンを作る関数。SQLAlchemyの心臓部分

# from sqlalchemy.orm import sessionmaker
DBと対話するためのセッションを作る工場(ファクトリー)。セッションを通じてCRUDを行う

# from sqlalchemy.ext.declarative import declarative_base
モデル(テーブル)を作るためのBaseクラスの元。class User(Base):とかで継承する

# engine = create_engine(f"sqlite:///{str(db_path.resolve())}")
SQLiteに接続するエンジン(実際のDBとやりとりするもの)を作成。sqlite:///はSQLite用のURL形式。
  例：sqlite:////Users/kano/.../database/db.sqlite


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
セッション(DBと会話するオブジェクト)を作る"工場関数"
autocommit=False👉明示的にcommitが筆意用
autoflush=False👉DBに自動で反映しない(安全)
bind=engine👉この工場から作られるSessionはengineを使う
この工程で、fastapiのエンドポイントからdb=sessionLocal()とすると「DBとやりとりできるSessionオブジェクト」が作れる

# Base = declarative_base()
SQLAlchemyのモデルはBaseを継承して作る。
例  class Url(Base):
      __tablename__ = "urls"
      id = Column(Integer, primary_key=True)
Alembicがテーブルを自動認識するためにも必須

# def get_db() ...
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
ここがFastAPIとSQLAlchemyの一番大事な接続ポイント！
## db = SessionLocal()
セッション(DBとの接続)を作る
## yield db
FastAPIに「このdbセッションを渡す」の意味
  def endpoint(db: Session = Depends(get_db)):
👆このときに使われる
## finally: db.close()
エンドポイントの処理が終わった後に必ずセッションを閉じてメモリリークを防ぐ