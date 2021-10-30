from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from apps.accounts.constants import COUNTER_TWEET
from apps.threads.models import AbstractTwitterUser


class User(AbstractTwitterUser, AbstractUser):
    """
    User model
    """
    due_premium_date = models.DateTimeField(null=True, blank=True)

    def extend_premium(self, days: int):
        """
        Add days to due premium date
        """
        if self.due_premium_date:
            self.due_premium_date = self.due_premium_date + timezone.timedelta(days=days)
        else:
            self.due_premium_date = timezone.now() + timezone.timedelta(days=days)
        self.save()

    @admin.display(
        boolean=True,
        ordering='due_premium_date',
        description='Is premium?',
    )
    def is_premium(self) -> bool:
        """
        Show if the premium date is due or not
        """
        if self.is_staff or self.is_superuser:
            return True
        if self.due_premium_date:
            return timezone.now() <= self.due_premium_date
        return False

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
