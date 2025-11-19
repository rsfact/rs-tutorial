# ①sqlite3.connect("db.sqlite")
conn = sqlite3.connect("db.sqlite")
同じフォルダに db.sqlite というファイルがあればそれを開く。なければ 新しくファイルを作る！
SQLiteは“ファイル型DB”だから、この1行だけで DB が存在するようになる✨

# ② CREATE TABLE IF NOT EXISTS urls (...)
CREATE TABLE IF NOT EXISTS urls (
urls というテーブル（表）を作る
すでに存在するなら作らない（IF NOT EXISTS）

# ③ id INTEGER PRIMARY KEY AUTOINCREMENT
id INTEGER PRIMARY KEY AUTOINCREMENT,
INTEGER（整数型）
PRIMARY KEY（主キー＝唯一のID）
AUTOINCREMENT（自動で1,2,3,...と増える）
👉 1件登録するたびに勝手にIDが増えるカラム！

# ④ key TEXT UNIQUE NOT NULL
key TEXT UNIQUE NOT NULL,
TEXT（文字列）
UNIQUE（重複禁止）
NOT NULL（絶対に空ではダメ）
👉 短縮URLのキー（from_name や uuid代わり）に相当するカラム
例えば
/u/line
/u/kanoko
/u/cute
みたいに URL の「キー」として使われるやつ🗝️

# ⑤ target_url TEXT NOT NULL
target_url TEXT NOT NULL,
TEXT（文字列）
NULL不可
👉 実際にリダイレクトするURL
例：
https://line.me/ti/p/xxxx
https://kanoko.xyz

# ⑥ created_at TEXT NOT NULL
created_at TEXT NOT NULL
TEXT（文字列）
空値禁止
👉 作成日時（ISO8601 文字列）
例：2025-11-19T15:41:21.234

# ⑦ commit & close
conn.commit()
conn.close()


commit：テーブル作成の変更をファイルに保存

close：DBを閉じる