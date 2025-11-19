from datetime import datetime
from app.db import get_db

def find_by_from_name(from_name: str):
    """
    from_name の重複チェックや検索に使う
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM urls WHERE from_name = ?", (from_name,))
    row = cursor.fetchone()

    conn.close()

    return row


def create_short_url(from_name: str, to_url: str):
    """
    新しい短縮URLの作成
    """
    conn = get_db()
    cursor = conn.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO urls (from_name, to_url, count, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (from_name, to_url, 0, created_at)
    )

    conn.commit()
    conn.close()

    return {
        "from_name": from_name,
        "to_url": to_url,
        "count": 0,
        "created_at": created_at
    }



def increment_count_and_get_url(from_name: str):
    """
    リダイレクト時に count を +1 して、飛び先のURLを返す
    """
    conn = get_db()
    cursor = conn.cursor()

    # URL取得
    cursor.execute("SELECT to_url, count FROM urls WHERE from_name = ?", (from_name,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    new_count = row["count"] + 1

    # count を更新
    cursor.execute(
        "UPDATE urls SET count = ? WHERE from_name = ?",
        (new_count, from_name)
    )

    conn.commit()
    conn.close()

    return row["to_url"]
