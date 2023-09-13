## Установка local
Склонировать репозиторий командой:
```
git clone git@github.com:kvadimas/foodgram-project-react.git
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
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
## Импорт csv
Чтоб заполнить базу ингридеентами запустите:
```
python3 manage.py import_csv
```
или:
```
python3 manage.py import_json
```