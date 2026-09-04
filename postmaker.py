import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]

model = "mistral-medium-latest"

client = Mistral(api_key=MISTRAL_API_KEY)


def format_post(article: dict) -> dict:
    """
    Принимает одну статью в формате, который отдаёт habrparser.parser():
    {"title": ..., "article": ..., "author": ..., "body": ...}
    Возвращает готовый пост.
    """
    response = client.chat.complete(
        model=model,
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

    generated_text = response.choices[0].message.content

    return {
        "title": article["title"],
        "url": article["article"],
        "author_url": article["author"],
        "text": generated_text,
    }
