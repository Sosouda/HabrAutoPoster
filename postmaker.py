import os
import time
from dotenv import load_dotenv
from mistralai.client import Mistral
from mistralai.client.errors import SDKError

load_dotenv()

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-medium-latest"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 20
SECONDS_BETWEEN_REQUESTS = 5

client = Mistral(api_key=MISTRAL_API_KEY)


def format_post(article: dict) -> dict:
    """
    Принимает одну статью в формате, который отдаёт habrparser.parser():
    {"title": ..., "article": ..., "author": ..., "body": ...}
    Возвращает готовый пост.
    """
    response = None
    for attempt in range(1, MAX_RETRIES + 1):
        time.sleep(SECONDS_BETWEEN_REQUESTS)
        try:
            response = client.chat.complete(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Ты — профессиональный контент-менеджер IT-канала."
                            " Твоя задача — прочитать статью с Хабра и сделать из неё сочный, структурированный пост для Telegram."
                            "Правила:1. Придумай цепляющий заголовок.2. Выдели 3-4 главных тезиса или практических вывода."
                            "3. Используй списки (буллеты) и эмодзи как визуальные якоря (но не перебарщивай)."
                            "4. Тон автора — экспертный, но дружелюбный (для разработчиков)."
                            "5. Жесткое ограничение: весь текст должен быть не длиннее 2500 символов."
                            "Структура у поста должна быть такая: сначала заголовок статьи,потом выжимка на 1-2 минуты чтения поста,"
                            " снизу ссылка вшита в 'читать далее' и снизу 'автор статьи: (тут ник автора тоже как ссылка)'"
                            f"Вот статья с которой ты работаешь: {article}."
                        ),
                    },
                ],
            )
            break
        except SDKError as e:
            is_rate_limit = "429" in str(e) or "rate_limited" in str(e)
            if is_rate_limit and attempt < MAX_RETRIES:
                print(f"[format_post] Rate limit, попытка {attempt}/{MAX_RETRIES}, жду {RETRY_DELAY_SECONDS}с...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            raise

    generated_text = response.choices[0].message.content

    return {
        "title": article["title"],
        "url": article["article"],
        "author_url": article["author"],
        "text": generated_text,
    }