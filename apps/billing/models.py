import hashlib

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from apps.core.models import SingletonModel, TimeStampedModel
from . import constants


class BillingConfig(SingletonModel):
    price_monthly = models.FloatField()
    price_yearly = models.FloatField()

    def __str__(self) -> str:
        return 'Billing config'


class Transaction(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    number = models.CharField(max_length=255)
    state = models.CharField(
        max_length=15,
        default=constants.BILLING_STATE[0][0],
        choices=constants.BILLING_STATE
    )

    # billing
    amount = models.FloatField(default=1)
    days = models.IntegerField(default=30)

    # QvaPay related
    qvapay_id = models.CharField(max_length=255, null=True, blank=True)
    qvapay_url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.number)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.number = hashlib.sha256(
                str(str(now()) + str(self.id)).encode()
            ).hexdigest()[:10]
        return super(Transaction, self).save(*args, **kwargs)
