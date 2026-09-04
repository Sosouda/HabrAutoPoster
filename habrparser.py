import requests
import unicodedata
from bs4 import BeautifulSoup

def parser():
    """Парсер берет статьи с сайта ХАБР у которых теги есть в списке желаемых.
        После этого для каждой подходящей создается словарь
        {название статьи:.., ссылка на статью:.., автор:.., текст статьи:..}
        и записывается в массив."""
    list_of_notes = []
    link = 'https://habr.com/ru/rss/articles/'
    req = requests.get(link)
    soup = BeautifulSoup(req.content, 'html.parser')

    items = soup.find_all('item')
    list_of_themes = (
        'bcrypt',  'аутентификация', 'рекомендательные системы',
        'microfrontends', 'web-разработка', 'микрофронтенд',
        'машинный перевод', 'opus', 'sol', 'flash', 'FastAPI', 'самописные инструменты',
        'GitHub' 'ИИ-агенты', 'искусственный интеллект', 'LLM', 'GPT', 'Claude', 'Gemini', 'DeepSeek',
        'AI-модели', 'reasoning', 'маршрутизация моделей', 'multi-model orchestration', 'LiteLLM',
        'LLM', 'Anthropic', 'OpenAI', 'Claude', 'CLIProxyAPI', 'LLM gateway', 'API gateway', 'опенсорс',
        'микроавтоматизация', 'автоматизация рутины','хакатон', 'боты', 'qwen', 'grok', 'Машинное обучение',
        'Data Engineering', 'ai-агенты','Python'
    )

    for item in items:
        if item.category.text in list_of_themes:

            curlink = item.guid.text
            resp = requests.get(curlink)
            soup = BeautifulSoup(resp.content, 'html.parser')
            title = soup.find('h1')
            author = soup.find('a', class_="tm-user-info__username").get('href')
            body = soup.find('article')
            clean_title = unicodedata.normalize("NFKD", title.text)
            clean_body = unicodedata.normalize("NFKD", body.text)
            list_of_notes.append({'title': clean_title, 'article':item.guid.text, 'author': 'https://habr.com'+author, 'body': clean_body})
    return list_of_notes

