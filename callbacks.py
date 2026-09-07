"""
callbacks.py

Callback-функции для RQ должны лежать в отдельном, нормально
импортируемом модуле НЕ в файле, который
запускается напрямую (python3 producer.py делает его "__main__",
а воркер не может импортировать функцию из чужого __main__).
"""

from redis_conn import redis_conn
from rq import Queue

from tasks import publish_to_telegram
from slots import get_next_slot

publish_queue = Queue("publish", connection=redis_conn)


def on_format_success(job, connection, result, *args, **kwargs):
    """
    Срабатывает автоматически, когда format_post успешно отработал.
    result — словарь поста, который вернул postmaker.format_post().
    """
    next_slot = get_next_slot(connection)
    publish_queue.enqueue_at(next_slot, publish_to_telegram, result)
    print(f"[callbacks] '{result['title']}' запланирован на {next_slot} UTC")
