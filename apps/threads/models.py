from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class AbstractTwitterUser(models.Model):
    """
    A model to reuse the twitter fields
    """
    twitter_token = models.CharField(max_length=100)
    twitter_token_secret = models.CharField(max_length=100)
    banner_url = models.URLField()
    image_url = models.URLField()

    class Meta:
        abstract = True


class Thread(TimeStampedModel):
    tweets = models.CharField('Tweets', max_length=2800)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
