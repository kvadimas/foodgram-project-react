# Foodgram

## Описание
Проект Foodgram - сайт, на котором пользователи будут публиковать рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других
авторов. Пользователям также будет доступна возможность скачать «Список
покупок».

## Стек технологий
Python 3, Django REST Framework, Nginx, PostgresSQL, Docker, GitHub Actions

## Установка
Установка осуществляется автоматически после коммита в master.
Для создания суперпользователя нужно:
- Зайти на удаленный сервер.
- Перейти в папку с docker-compose.production.yml
- Выполнить
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

## Ручная установка
- Установить на сервере Docker, Docker Compose:
```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```
- Скопировать на сервер файл docker-compose.production.yml
- Создать файл .env:
```
nano .env
```
Скопировать и заполнить константы (не забудте сохранить):
```
ALLOWED_HOSTS=158.160.27.77 127.0.0.1 localhost fieryshop.ru
SECRET_KEY              # секретный ключ Django проекта
DEBUG                   # False - если дебаг не нужен и True - если нужен
ALLOWED_HOSTS           # точки доступа для бекенда

POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user_12345
POSTGRES_PASSWORD=foodgram_password_12345
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
```
- Выполнить:
```
sudo docker compose -f docker-compose.production.yml up -d
sudo docker compose -f docker-compose.production.yml exec backepython manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backepython manage.py import_json
sudo docker compose -f docker-compose.production.yml exec backepython manage.py collectstatic
```
- Настроить Nginx.

## Автор backend'а:
[kvadimas](https://github.com/kvadimas)
