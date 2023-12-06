#!/bin/bash

cd /opt/fume/
source ~/venvs/fume/bin/activate

gunicorn --certfile=/etc/letsencrypt/live/fumetsu.pl/fullchain.pem --keyfile=/etc/letsencrypt/live/fumetsu.pl/privkey.pem --bind 0.0.0.0:443 app:app

