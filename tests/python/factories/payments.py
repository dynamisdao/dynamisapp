import factory

from dynamis.apps.payments.models import SmartDeposit, PremiumPayment, EthAccount, SmartDepositRefund, TokenAccount


class SmartDepositFactory(factory.DjangoModelFactory):
    eth_account = factory.SubFactory('factories.payments.EthAccountFactory')
    policy = factory.SubFactory('factories.policy.PolicyApplicationFactory')
    amount = 7.5

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
