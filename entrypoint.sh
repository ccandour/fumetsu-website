#!/bin/sh

# collect all static files to the root directory
python3 manage.py collectstatic --no-input

# apply all migrations to the database
python3 manage.py makemigrations
python3 manage.py migrate

# start the gunicorn worker process at the defined port
gunicorn core.wsgi:application --bind 0.0.0.0:8000 &

wait