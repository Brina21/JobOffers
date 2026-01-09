#!/bin/sh

cd /code

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn --chdir /code --bind 0.0.0.0:8000 joboffers.wsgi:application