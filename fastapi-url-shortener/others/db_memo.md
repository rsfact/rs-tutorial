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