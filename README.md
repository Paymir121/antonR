
# Сайт визитка для стройки
### Описание
Благодаря этому проекту можно  улучшить комьюните по методичке @Травомана
### Технологии
Python 3.7
Django 2.2.19
### Запуск проекта в dev-режиме

```
- Установите и активируйте виртуальное окружение WINDOWS
python -m venv venv
source venv/Scripts/activate
- Установите зависимости из файла requirements.txt
pip install -r requirements.txt

- В папке с файлом manage.py выполните команду:
source venv/Scripts/activate
cd antonR
python manage.py runserver
http://127.0.0.1:8000/
```
- Установите и активируйте виртуальное окружение MAC OS
python3 -m venv venv
source venv/bin/activate
- Установите зависимости из файла requirements.txt
pip install -r requirements.txt

- В папке с файлом manage.py выполните команду:
source venv/bin/activate
cd antonR
python3 manage.py runserver
http://127.0.0.1:8000/

```
Установить миграции
python manage.py makemigrations
python manage.py migrate   

pip install Pillow

python manage.py test
Создать суперпользователя
python manage.py createsuperuser
### Авторы
Никки и Никонор
