#!/bin/sh

# collect all static files to the root directory
python3 manage.py collectstatic --no-input

# start the gunicorn worker process at the defined port
gunicorn core.wsgi:application --bind 0.0.0.0:8000 &

wait