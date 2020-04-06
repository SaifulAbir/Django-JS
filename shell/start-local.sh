#!/usr/bin/env bash
source venv/bin/activate
pip install -r requirements/req-dev.txt
python manage.py makemigrations
python manage.py migrate
export DJANGO_SETTINGS_MODULE="p7.settings_local"
python manage.py runserver 0:8000

