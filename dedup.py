import sqlite3
from pathlib import Path
from urllib.parse import urlsplit
DB_PATH = Path(__file__).parent / "seen_articles.db"

def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS seen_articles (
            url TEXT PRIMARY KEY,
            seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conn

def normalize_url(url: str) -> str:
    """
    Хабр иногда отдаёт в RSS один и тот же URL статьи с разными
    query-параметрами между заходами (например, ?utm_source=...).
    """
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}{parts.path.rstrip('/')}"


def is_new(article_url: str) -> bool:
    """
    Возвращает True, если статья ещё не обрабатывалась, и сразу
    записывает её как обработанную.

    PRIMARY KEY на url гарантирует, что повторная вставка того же
    URL просто провалится (IntegrityError).
    """
    clean_url = normalize_url(article_url)
    conn = _get_connection()
    try:
        conn.execute("INSERT INTO seen_articles (url) VALUES (?)", (clean_url,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()