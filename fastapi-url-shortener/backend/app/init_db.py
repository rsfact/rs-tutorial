import sqlite3

conn = sqlite3.connect("db.sqlite")

conn.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_name TEXT UNIQUE NOT NULL,
    to_url TEXT NOT NULL,
    count INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
""")

conn.commit()
conn.close()
