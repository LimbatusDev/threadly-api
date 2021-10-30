celery -A config worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
