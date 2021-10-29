from django.apps import AppConfig


class ThreadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.threads'
    label = 'threads'
    verbose_name = 'Threads app'
