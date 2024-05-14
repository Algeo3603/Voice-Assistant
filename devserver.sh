#!/bin/sh
# source .venv/bin/activate
cd mysite
source venv/bin/activate
python manage.py runserver
# python mysite/manage.py runserver $PORT
