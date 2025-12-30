#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Postgres is up"

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py initdata

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 120
