from __future__ import unicode_literals

from django.db import models

from dynamis import settings
from dynamis.core.models import TimestampModel


class EthAccount(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='eth_accounts')
    is_active = models.BooleanField(default=True)
    eth_balance = models.FloatField(default=0.0)
    eth_address = models.URLField(null=True)


class TokenAccount(TimestampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='token_account')
    immature_tokens_balance = models.FloatField(default=0.0)
    mature_tokens_balance = models.FloatField(default=0.0)
    disabled = models.BooleanField(default=False)


class SmartDeposit(TimestampModel):
    eth_account = models.ForeignKey(EthAccount, related_name='smart_deposits')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='smart_deposit')
    is_confirmed = models.BooleanField(default=False)
    amount = models.FloatField()


class SmartDepositRefund(TimestampModel):
    smart_deposit = models.ForeignKey(SmartDeposit, related_name='smart_deposit_refunds')
    is_confirmed = models.BooleanField(default=False)
    amount = models.FloatField()


class PremiumPayment(TimestampModel):
    eth_account = models.ForeignKey(EthAccount, related_name='premium_payments')
    is_confirmed = models.BooleanField(default=False)
    amount = models.FloatField()


class FillEthOperation(TimestampModel):
    eth_account = models.ForeignKey(EthAccount, related_name='fill_eth_operations')
    amount = models.FloatField()
    is_confirmed = models.BooleanField(default=False)


class WithdrawalEthOperation(TimestampModel):
    eth_account = models.ForeignKey(EthAccount, related_name='withdrawal_eth_operations')
    amount = models.FloatField()
    is_confirmed = models.BooleanField(default=False)


class BuyTokenOperation(TimestampModel):
    eth_account = models.ForeignKey(EthAccount, related_name='buy_token_operations')
    token_account = models.ForeignKey(TokenAccount, related_name='buy_token_operations')
    amount = models.FloatField()


class SellTokenOperation(TimestampModel):
    eth_account = models.ForeignKey(EthAccount, related_name='sell_token_operations')
    token_account = models.ForeignKey(TokenAccount, related_name='sell_token_operations')
    amount = models.FloatField()
