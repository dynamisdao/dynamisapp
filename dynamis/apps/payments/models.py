from __future__ import unicode_literals

import datetime
from constance import config
from django.db import models
from django.utils import timezone
from django_fsm import FSMIntegerField, transition

from dynamis import settings
from dynamis.apps.payments.business_logic import refresh_usd_eth_exchange_rate
from dynamis.core.models import TimestampModel, EthTransaction
from dynamis.utils.math import approximately_equal

WAIT_FOR_TX_STATUS_INIT = 0
WAIT_FOR_TX_STATUS_WAITING = 1
WAIT_FOR_TX_STATUS_RECEIVED = 2

WAIT_FOR_TX_STATUS = (
    (WAIT_FOR_TX_STATUS_INIT, 'init'),
    (WAIT_FOR_TX_STATUS_WAITING, 'wait_for_tx'),
    (WAIT_FOR_TX_STATUS_RECEIVED, 'received')
)


class EthAccount(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='eth_accounts')
    rpc_node_host = models.URLField(null=True)

    # TODO maybe not used
    is_active = models.BooleanField(default=True)
    eth_balance = models.FloatField(default=0.0)
    # TODO user provide his eth_address at every payment, store in SmartDeposit model - 'from_address'
    eth_address = models.CharField(null=True, max_length=1023)


class TokenAccount(TimestampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='token_account')
    immature_tokens_balance = models.FloatField(default=0.0)
    mature_tokens_balance = models.FloatField(default=0.0)
    disabled = models.BooleanField(default=False)


class SmartDeposit(TimestampModel):
    WAIT_FOR_TX_STATUS_INIT = WAIT_FOR_TX_STATUS_INIT
    WAIT_FOR_TX_STATUS_WAITING = WAIT_FOR_TX_STATUS_WAITING
    WAIT_FOR_TX_STATUS_RECEIVED = WAIT_FOR_TX_STATUS_RECEIVED

    WAIT_FOR_TX_STATUS = WAIT_FOR_TX_STATUS

    # TODO delete null = True after development real smart deposits
    eth_account = models.ForeignKey(EthAccount, related_name='smart_deposits', null=True)
    policy = models.OneToOneField('policy.PolicyApplication', related_name='smart_deposit', primary_key=True)
    # is_confirmed = models.BooleanField(default=False)
    amount = models.FloatField(default=0)
    amount_dollar = models.FloatField(null=True)
    cost = models.FloatField(null=True)
    cost_dollar = models.FloatField(null=True)
    exchange_rate_at_invoice_time = models.FloatField(null=True)
    wait_for = models.DateTimeField(null=True)
    from_address = models.CharField(max_length=1023, null=True)
    state = FSMIntegerField(default=WAIT_FOR_TX_STATUS_INIT, protected=True, choices=WAIT_FOR_TX_STATUS)
    eth_tx = models.OneToOneField(EthTransaction, related_name='smart_deposit', null=True)

    @property
    def cost_wei(self):
        if self.cost:
            return int(self.cost * 1000000000000000000)

    def save(self, *args, **kwargs):
        raw_cost = self.cost_dollar / config.DOLLAR_ETH_EXCHANGE_RATE
        self.cost = round(raw_cost, 3)
        super(SmartDeposit, self).save(*args, **kwargs)

    def check_smart_deposit_amount(self):
        if approximately_equal(self.amount, self.cost, config.TX_VALUE_DISPERSION):
            return True

    @transition(field=state, source=WAIT_FOR_TX_STATUS_INIT, target=WAIT_FOR_TX_STATUS_WAITING)
    def init_to_wait(self):
        refresh_usd_eth_exchange_rate()
        self.wait_for = timezone.now() + datetime.timedelta(
            minutes=config.WAIT_FOR_RECEIVE_SMART_DEPOSIT_MINUTES)
        self.exchange_rate_at_invoice_time = config.DOLLAR_ETH_EXCHANGE_RATE
        self.save()

    @transition(field=state, source=WAIT_FOR_TX_STATUS_WAITING, target=WAIT_FOR_TX_STATUS_INIT)
    def wait_to_init(self):
        refresh_usd_eth_exchange_rate()
        self.cost = self.cost_dollar / config.DOLLAR_ETH_EXCHANGE_RATE
        self.save()

    @transition(field=state, source=WAIT_FOR_TX_STATUS_WAITING, target=WAIT_FOR_TX_STATUS_RECEIVED,
                conditions=[check_smart_deposit_amount])
    def wait_to_received(self):
        self.policy.submit_to_p2p_review()
        self.policy.save()


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
    WAIT_FOR_TX_STATUS_INIT = WAIT_FOR_TX_STATUS_INIT
    WAIT_FOR_TX_STATUS_WAITING = WAIT_FOR_TX_STATUS_WAITING
    WAIT_FOR_TX_STATUS_RECEIVED = WAIT_FOR_TX_STATUS_RECEIVED

    WAIT_FOR_TX_STATUS = WAIT_FOR_TX_STATUS

    token_account = models.ForeignKey(TokenAccount, related_name='buy_token_operations')
    eth_tx = models.OneToOneField(EthTransaction, related_name='buy_token_operation', null=True)
    amount = models.FloatField(null=True)
    count = models.IntegerField()
    cost = models.FloatField(null=True)
    token_cost_at_invoice_time = models.FloatField(null=True)
    from_address = models.CharField(max_length=1023)
    wait_for = models.DateTimeField(null=True)
    state = FSMIntegerField(default=WAIT_FOR_TX_STATUS_INIT, protected=True, choices=WAIT_FOR_TX_STATUS)

    @property
    def cost_wei(self):
        if self.cost:
            return int(self.cost * 1000000000000000000)

    def save(self, *args, **kwargs):
        if self.state != WAIT_FOR_TX_STATUS_RECEIVED:
            self.cost = config.EHT_TOKEN_EXCHANGE_RATE * self.count
        super(BuyTokenOperation, self).save(*args, **kwargs)

    def check_buy_token_operation(self):
        if self.eth_tx.hash and approximately_equal(self.amount, self.cost, config.TX_VALUE_DISPERSION):
            return True

    @transition(field=state, source=WAIT_FOR_TX_STATUS_INIT, target=WAIT_FOR_TX_STATUS_WAITING)
    def init_to_wait(self):
        self.wait_for = timezone.now() + datetime.timedelta(
            minutes=config.WAIT_FOR_BUY_TOKEN_TX_MINUTES)
        self.token_cost_at_invoice_time = config.EHT_TOKEN_EXCHANGE_RATE
        self.save()

    @transition(field=state, source=WAIT_FOR_TX_STATUS_WAITING, target=WAIT_FOR_TX_STATUS_INIT)
    def wait_to_init(self):
        pass

    @transition(field=state, source=WAIT_FOR_TX_STATUS_WAITING, target=WAIT_FOR_TX_STATUS_RECEIVED,
                conditions=[check_buy_token_operation])
    def wait_to_received(self):
        self.token_account.immature_tokens_balance += self.amount
        self.token_account.save()


class SellTokenOperation(TimestampModel):
    eth_account = models.ForeignKey(EthAccount, related_name='sell_token_operations')
    token_account = models.ForeignKey(TokenAccount, related_name='sell_token_operations')
    amount = models.FloatField()


class MakeBetOperation(TimestampModel):
    assessor_token_account = models.ForeignKey(TokenAccount, related_name='make_bet_operations')
    internal_contractor_token_account = models.ForeignKey(TokenAccount, related_name='receive_bet_operations')
    risk_assessment_task = models.OneToOneField('policy.RiskAssessmentTask', related_name='make_bet_operations')
    amount = models.FloatField(null=True)
