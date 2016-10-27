import datetime as datetime
import factory

from dynamis.apps.payments.models import SmartDeposit, PremiumPayment, EthAccount, SmartDepositRefund, TokenAccount, \
    BuyTokenOperation
from dynamis.core.models import EthTransaction
from dynamis.settings import TEST_SYSTEM_ETH_ADDRESS


class SmartDepositFactory(factory.DjangoModelFactory):
    eth_account = factory.SubFactory('factories.payments.EthAccountFactory')
    policy = factory.SubFactory('factories.policy.PolicyApplicationFactory')
    # amount = 7.5
    cost_dollar = 20

    class Meta:
        model = SmartDeposit


class SmartDepositRefundFactory(factory.DjangoModelFactory):
    smart_deposit = factory.SubFactory('factories.payments.SmartDepositFactory')
    amount = 7.5

    class Meta:
        model = SmartDepositRefund


class PremiumPaymentFactory(factory.DjangoModelFactory):
    eth_account = factory.SubFactory('factories.payments.EthAccountFactory')
    is_confirmed = False
    amount = 2.5

    class Meta:
        model = PremiumPayment


class EthAccountFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')

    class Meta:
        model = EthAccount


class TokenAccountFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')

    class Meta:
        model = TokenAccount


class EthTxFactory(factory.DjangoModelFactory):
    from_address = "0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86"
    to_address = TEST_SYSTEM_ETH_ADDRESS
    hash = "0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904"
    value = 33868806240000000000
    datetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    confirmations = 373300

    class Meta:
        model = EthTransaction


class BuyTokenOperationFactory(factory.DjangoModelFactory):
    token_account = factory.SubFactory('factories.accounts.TokenAccountFactory')
    count = 1

    class Meta:
        model = BuyTokenOperation
