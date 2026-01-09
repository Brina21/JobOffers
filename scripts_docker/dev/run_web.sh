#!/bin/sh
cd /code
# collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000