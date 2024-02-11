#!/bin/sh

echo "Waiting for postgres..."
# while ! nc -z $DB_HOST_DEFAULT $DB_PORT_DEFAULT; do
#     sleep 0.1
# done

echo "PostgreSQL started"

python manage.py makemigrations
python manage.py migrate
python manage.py create_admin 
python manage.py collectstatic --no-input
# python manage.py runserver

gunicorn users.wsgi:application --bind 0.0.0.0:8000 --reload