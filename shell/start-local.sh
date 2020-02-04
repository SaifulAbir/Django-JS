#!/usr/bin/env bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver --insecure 0:80

