import sqlite3
from pathlib import Path

from app.core import settings



def get_db():
    db_path = Path(__file__).parent.parent.parent / settings.SQLITE_PATH
    
    conn = sqlite3.connect(str(db_path.resolve()))
    conn.row_factory = sqlite3.Row
    return conn