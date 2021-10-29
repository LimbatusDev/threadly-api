from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.constants import COUNTER_TWEET
from apps.threads.models import AbstractTwitterUser


class User(AbstractTwitterUser, AbstractUser):
    """
    User model
    """
    twitter_token = models.CharField(max_length=100)
    twitter_token_secret = models.CharField(max_length=100)
    banner_url = models.URLField()
    image_url = models.URLField()

    class Meta:
        ordering = ['username']

    def __str__(self) -> str:
        return self.get_full_name() or self.username

    def activate(self):
        self.is_active = True


class UserConfiguration(models.Model):
    tweet_sends = models.IntegerField(default=0)
    counter = models.CharField(max_length=10, choices=COUNTER_TWEET, default=COUNTER_TWEET[0][0])
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
