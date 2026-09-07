# HabrAutoPoster

Проект реализует выбор статей с Хабр по интересующим тегам,
преобразование в посты для телеграм через Groq API и выкладывание
постов в канал автономно.

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Deploy и CI/CD](#deploy-и-ci/cd)

## Технологии
- [Python](https://www.python.org/doc/)
- [Redis](https://redis.io)
- [Groq Api](https://groq.com/platform)


## Использование

Клонируйте репозиторий с помощью команды:
```sh
$ git clone https://github.com/Sosouda/HabrAutoPoster.git
```

### Создание виртуального окружения и установка зависимостей
Для установки зависимостей, выполните команду:
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
### Создание билда
Создайте .env файл и заполните как в env.example: 
```sh
$ nano .env
```
Отредактируйте **list_of_themes** в файле **habrparser.py**
и поле **content** в **postmaker.py** под ваши задачи
```sh
$ nano habrparser.py
$ nano postmaker.py
```

## Deploy и CI/CD
### Запуск redis, подготовка врокеров
Чтобы запустить redis установите docker:
```sh
$ -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
$ sudo usermod -aG docker $USER
$ docker --version
```
Запустите redis в контейнере:
```sh
$ docker run -d -p 6379:6379 redis
$ docker ps #должен быть показан запущенный redis
$ sudo apt install redis-tools -y 
$ redis-cli -h localhost -p 6379 ping #Должно вернуть PONG
```
Создайте воркеров для сбора статей и публикации:
```sh
$ sudo nano /etc/systemd/system/habr-worker-format.service
```
Вставьте 
```commandline
[Unit]
Description=RQ worker format
After=network.target

[Service]
WorkingDirectory=/home/habrbot/HabrAutoPoster
EnvironmentFile=/home/habrbot/HabrAutoPoster/.env
ExecStart=/home/habrbot/HabrAutoPoster/.venv/bin/rq worker format
Restart=always
RestartSec=10
StartLimitIntervalSec=0
User=habrbot

[Install]
WantedBy=multi-user.target
```
```sh
$ sudo nano /etc/systemd/system/habr-worker-publish.service
```
Вставьте 
```commandline
[Unit]
Description=RQ worker publish
After=network.target

[Service]
WorkingDirectory=/home/habrbot/HabrAutoPoster
EnvironmentFile=/home/habrbot/HabrAutoPoster/.env
ExecStart=/home/habrbot/HabrAutoPoster/.venv/bin/rq worker publish --with-scheduler
Restart=always
RestartSec=10
StartLimitIntervalSec=0
User=habrbot

[Install]
WantedBy=multi-user.target
```
Запустите воркеров
```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now habr-worker-format
$ sudo systemctl enable --now habr-worker-publish
```
Проверьте работу 
```sh
$ sudo systemctl status habr-worker-format #Active: active (running)
$ sudo systemctl status habr-worker-publish #Active: active (running)
```
### Запуск программы и переход на автоматическую работу
```sh
$ python3 producer.py
$ journalctl -u habr-worker-format -n 30 --no-pager
```
При ошибке в логах уберите со статей пометку "выложенные"
```sh
$ redis-cli
```
```redis-cli
SMEMBERS habr_bot:seen_articles 
SREM habr_bot:seen_articles "ссылка на статью"
```
Перезагрузите воркера
```sh
$ sudo systemctl restart habr-worker-format
```
Если никаких ошибок не было
```sh
$ crontab -e
```
Впишите следующую команду(либо другую на ваше усмотрение):
```
0 */6 * * * cd /home/habrbot/HabrAutoPoster && /home/habrbot/HabrAutoPoster/.venv/bin/python3 producer.py >> /home/habrbot/HabrAutoPoster/producer.log 2>&1
```
