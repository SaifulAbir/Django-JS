#!/usr/bin/env bash
cd /var/projectseven/web/
source venv/bin/activate
export DJANGO_SETTINGS_MODULE="assessment.settings_prod"
python manage.py runserver 0:8080 > projectseven.log

