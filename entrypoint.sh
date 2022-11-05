#!/bin/sh
gunicorn config.wsgi:application -b :8000 --log-file /code/logs/gunicorn.log
