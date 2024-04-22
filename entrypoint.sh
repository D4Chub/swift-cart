#!/bin/bash

# Выполнение миграций
echo "Выполнение миграций..."
python service/manage.py makemigrations
python service/manage.py migrate

