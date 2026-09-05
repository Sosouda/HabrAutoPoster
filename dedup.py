from urllib.parse import urlsplit
from redis import Redis

SEEN_KEY = "habr_bot:seen_articles"


def normalize_url(url: str) -> str:
    """
    Хабр иногда отдаёт в RSS один и тот же URL статьи с разными
    query-параметрами между заходами (например, ?utm_source=...).
    """
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}{parts.path.rstrip('/')}"


def is_new(redis_conn: Redis, article_url: str) -> bool:
    """
    Возвращает True, если статья ещё не обрабатывалась, и сразу
    помечает её как обработанную (атомарно, через SADD).
    """
    clean_url = normalize_url(article_url)
    added = redis_conn.sadd(SEEN_KEY, clean_url)
    return added == 1