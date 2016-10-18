from constance import config
from django.utils import timezone

from dynamis.apps.payments.models import SmartDeposit, SMART_DEPOSIT_STATUS_WAITING


def test_check_wait_for_deposit_time(factories, mock_request_exchange_rate):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=0)
    assert deposit.wait_for is None
    deposit.init_to_wait()
    deposit = SmartDeposit.objects.get()

    assert deposit.wait_for > timezone.now()
    assert deposit.exchange_rate_at_invoice_time == config.DOLLAR_ETH_EXCHANGE_RATE
    assert config.DOLLAR_ETH_EXCHANGE_RATE == 12.686


def test_check_wait_to_init(factories, mock_request_exchange_rate):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=SMART_DEPOSIT_STATUS_WAITING)
    deposit.wait_to_init()

    assert config.DOLLAR_ETH_EXCHANGE_RATE == 12.686
