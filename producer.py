from redis import Redis
from rq import Queue

from habrparser import parser
from tasks import format_post, publish_to_telegram
from slots import get_next_slot
from dedup import is_new

redis_conn = Redis(host="localhost", port=6379, db=0)

format_queue = Queue("format", connection=redis_conn)
publish_queue = Queue("publish", connection=redis_conn)


def on_format_success(job, connection, result, *args, **kwargs):
    """
    Срабатывает автоматически, когда format_post успешно отработал.
    result — это словарь поста, который вернул postmaker.format_post().
    """
    next_slot = get_next_slot(connection)
    publish_queue.enqueue_at(next_slot, publish_to_telegram, result)
    print(f"[producer] '{result['title']}' запланирован на {next_slot} UTC")


def parse_and_enqueue():
    articles = parser()

    for article in articles:
        if not is_new(redis_conn, article["article"]):
            print(f"[producer] Пропущено (уже обработано): {article['title']}")
            continue

        format_queue.enqueue(format_post, article, on_success=on_format_success)
        print(f"[producer] В очередь оформления: {article['title']}")


if __name__ == "__main__":
    parse_and_enqueue()