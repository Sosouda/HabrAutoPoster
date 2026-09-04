from redis import Redis

SEEN_KEY = "habr_bot:seen_articles"


def is_new(redis_conn: Redis, article_url: str) -> bool:
    """
    Возвращает True, если статья ещё не обрабатывалась, и сразу
    помечает её как обработанную (атомарно, через SADD).
    """
    added = redis_conn.sadd(SEEN_KEY, article_url)
    return added == 1
