# Foodgram
## Описание
Проект Foodgram - сайт, на котором пользователи будут публиковать рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других
авторов. Пользователям также будет доступна возможность скачать «Список
покупок».
## Установка
Склонировать репозиторий командой:
```
git clone git@github.com:kvadimas/api_yamdb.git
```
Перейти в папку с проектом, установить виртуальное окружение и активировать его:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Перейти в папку:
```
cd api_yamdb/
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
## Документация
[Документация к API в формате Redoc.](http://127.0.0.1:8000/redoc/)
## Импорт csv
Чтоб заполнить базу ингридеентами запустите:
```
python3 manage.py import_csv
python3 manage.py import_json
```
или:
```
python3 manage.py import_json
```