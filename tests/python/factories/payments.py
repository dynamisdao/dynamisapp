import factory

from dynamis.apps.payments.models import SmartDeposit, PremiumPayment, EthAccount


class SmartDepositFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')
    is_confirmed = False
    amount = 7.5
    refunded = False

    class Meta:
        model = SmartDeposit


class PremiumPaymentFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')
    is_confirmed = False
    amount = 2.5

    class Meta:
        model = PremiumPayment


class EthAccountFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')

    class Meta:
        model = EthAccount
