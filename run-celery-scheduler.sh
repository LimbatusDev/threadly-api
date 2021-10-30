#!/bin/bash

celery -A config beat -l INFO -S django_celery_beat.schedulers:DatabaseScheduler
