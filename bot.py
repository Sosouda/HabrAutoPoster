import os
import requests
from dotenv import load_dotenv

load_dotenv()
def publish_to_telegram(post: dict) -> None:
    """
    Принимает пост из format_post() и публикует его в канал
    от имени бота через Telegram Bot API.
    """

    bot_token = os.environ["TG_BOT_TOKEN"]
    channel_id = os.environ["TG_CHANNEL_ID"]
    resp = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={
            "chat_id": channel_id,
            "text": post["text"],
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
        },
        timeout=30,
    )
    resp.raise_for_status()
    print(f"[publish] Опубликовано: {post['title']}")