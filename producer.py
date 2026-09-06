"""
producer.py

Продюсер: запускается по расписанию, дергает habrparser.parser(),
отфильтровывает уже виденные статьи и кладёт новые в очередь на оформление.
"""

from redis import Redis
from rq import Queue

from habrparser import parser
from tasks import format_post
from callbacks import on_format_success
from dedup import is_new

redis_conn = Redis(host="localhost", port=6379, db=0)
format_queue = Queue("format", connection=redis_conn)


def parse_and_enqueue():
    articles = parser()

    for article in articles:
        if not is_new(article["article"]):
            print(f"[producer] Пропущено (уже обработано): {article['title']}")
            continue

        format_queue.enqueue(format_post, article, on_success=on_format_success)
        print(f"[producer] В очередь оформления: {article['title']}")


if __name__ == "__main__":
    parse_and_enqueue()