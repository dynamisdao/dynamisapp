from __future__ import unicode_literals

from django.db import models

from dynamis import settings
from dynamis.core.models import TimestampModel


class EthAccount(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='eth_account')
    is_active = models.BooleanField(default=True)
    immature_tokens_balance = models.FloatField(default=0.0)
    mature_tokens_balance = models.FloatField(default=0.0)
    eth_address = models.URLField(null=True)


class SmartDeposit(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='smart_deposits')
    is_confirmed = models.BooleanField(default=False)
    amount = models.FloatField()
    refunded = models.BooleanField(default=False)


class PremiumPayment(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='premium_payments')
    is_confirmed = models.BooleanField(default=False)
    amount = models.FloatField()
