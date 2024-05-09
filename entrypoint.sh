#!/bin/bash

# Выполнение миграций
echo "Выполнение миграций..."
python service/manage.py makemigrations
python service/manage.py migrate

# Загрузка тестовый данных в бд
echo "Загрузка тестовых данных в бд..."
python service/manage.py loaddata service/db.json

