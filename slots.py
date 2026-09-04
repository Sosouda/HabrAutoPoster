from datetime import datetime, timedelta
from redis import Redis

NEXT_SLOT_KEY = "habr_bot:next_publish_slot"
INTERVAL = timedelta(hours=1)


def get_next_slot(redis_conn: Redis) -> datetime:
    """
    Возвращает время, на которое нужно запланировать следующую публикацию,
    и сразу сдвигает "курсор" на час вперёд для следующего вызова.
    """
    now = datetime.utcnow()
    raw = redis_conn.get(NEXT_SLOT_KEY)

    if raw is None:
        next_slot = now
    else:
        stored = datetime.fromisoformat(raw.decode())
        # если сохранённый слот уже в прошлом (бот не работал какое-то время) —
        # начинаем отсчёт от текущего момента, а не постим все сразу
        next_slot = stored if stored > now else now

    # резервируем этот слот и двигаем курсор на час вперёд
    redis_conn.set(NEXT_SLOT_KEY, (next_slot + INTERVAL).isoformat())
    return next_slot