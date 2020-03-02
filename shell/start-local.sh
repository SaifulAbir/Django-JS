#!/usr/bin/env bash
source venv/bin/activate
pip install -r requirements/req-dev.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0:8000

