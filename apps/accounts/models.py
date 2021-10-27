from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
