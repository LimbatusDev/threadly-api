from django.db import models
from django.conf import settings

from apps.core.models import TimeStampedModel


class Thread(TimeStampedModel):
    tweets = models.CharField('Tweets', max_length=2800)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO: agregar fecha de publicación
