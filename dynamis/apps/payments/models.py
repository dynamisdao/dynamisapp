from __future__ import unicode_literals

import datetime
from constance import config
from django.db import models
from django_fsm import FSMIntegerField, transition

from dynamis import settings
from dynamis.core.models import TimestampModel

SMART_DEPOSIT_STATUS_INIT = 0
SMART_DEPOSIT_STATUS_WAITING = 1
SMART_DEPOSIT_STATUS_RECEIVED = 2

SMART_DEPOSIT_STATUS = (
    (SMART_DEPOSIT_STATUS_INIT, 'init'),
    (SMART_DEPOSIT_STATUS_WAITING, 'wait_for_deposit'),
    (SMART_DEPOSIT_STATUS_RECEIVED, 'received')
)


class EthAccount(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='eth_accounts')
    is_active = models.BooleanField(default=True)
    eth_balance = models.FloatField(default=0.0)
    eth_address = models.CharField(null=True, max_length=1023)
    eth_node_host = models.URLField(null=True)


class TokenAccount(TimestampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='token_account')
    immature_tokens_balance = models.FloatField(default=0.0)
    mature_tokens_balance = models.FloatField(default=0.0)
    disabled = models.BooleanField(default=False)


class SmartDeposit(TimestampModel):
    # TODO delete null = True after development real smart deposits
    eth_account = models.ForeignKey(EthAccount, related_name='smart_deposits', null=True)
    policy = models.OneToOneField('policy.PolicyApplication', related_name='smart_deposit', primary_key=True)
    # is_confirmed = models.BooleanField(default=False)
    amount = models.FloatField()
    amount_dollar = models.FloatField(null=True)
    coast = models.FloatField(null=True)
    coast_dollar = models.FloatField(null=True)
    exchange_rate_at_invoice_time = models.FloatField(null=True)
    state = FSMIntegerField(default=SMART_DEPOSIT_STATUS_INIT, protected=True, choices=SMART_DEPOSIT_STATUS)
    wait_for = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        raw_coast = self.coast_dollar / config.DOLLAR_ETH_EXCHANGE_RATE
        self.coast = round(raw_coast, 3)
        super(SmartDeposit, self).save(*args, **kwargs)

    def check_smart_deposit_amount(self):
        if self.amount >= self.coast:
            return True

    @transition(field=state, source=SMART_DEPOSIT_STATUS_INIT, target=SMART_DEPOSIT_STATUS_WAITING)
    def init_to_wait(self):
        self.wait_for = datetime.datetime.now() + datetime.timedelta(
            minutes=config.WAIT_FOR_RECEIVE_SMART_DEPOSIT_MINUTES)
        self.exchange_rate_at_invoice_time = config.DOLLAR_ETH_EXCHANGE_RATE
        self.save()

    @transition(field=state, source=SMART_DEPOSIT_STATUS_WAITING, target=SMART_DEPOSIT_STATUS_INIT)
    def wait_to_init(self):
        pass

    @transition(field=state, source=SMART_DEPOSIT_STATUS_WAITING, target=SMART_DEPOSIT_STATUS_RECEIVED,
                conditions=[check_smart_deposit_amount])
    def wait_to_received(self):
        pass


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


class MakeBetOperation(TimestampModel):
    assessor_token_account = models.ForeignKey(TokenAccount, related_name='make_bet_operations')
    internal_contractor_token_account = models.ForeignKey(TokenAccount, related_name='receive_bet_operations')
    risk_assessment_task = models.OneToOneField('policy.RiskAssessmentTask', related_name='make_bet_operations')
    amount = models.FloatField(null=True)
