import sqlite3

sql_script = """
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id TEXT PRIMARY KEY,
    from_name TEXT NOT NULL UNIQUE,
    to_url TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
);
"""

def create_table(db_file: str):
    conn = sqlite3.connect(db_file)
    conn.executescript(sql_script)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table("db.sqlite")
