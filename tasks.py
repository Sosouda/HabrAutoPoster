"""
RQ кладёт в очередь ССЫЛКУ на функцию (по её пути импорта)
Это импортирует и вызывает воркер.
"""

from postmaker import format_post          # твоя функция: статья -> готовый пост
from bot import publish_to_telegram        # твоя функция: пост -> отправка в ТГ

__all__ = ["format_post", "publish_to_telegram"]
