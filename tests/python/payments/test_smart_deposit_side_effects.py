import json

from constance import config
from django.utils import timezone

from dynamis.apps.payments.models import SmartDeposit, WAIT_FOR_TX_STATUS_WAITING, WAIT_FOR_TX_STATUS_INIT
from dynamis.apps.policy.models import PolicyApplication, POLICY_STATUS_ON_P2P_REVIEW, POLICY_STATUS_SUBMITTED


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
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING)
    deposit.wait_to_init()

    assert config.DOLLAR_ETH_EXCHANGE_RATE == 12.686


def test_wait_to_received(factories, policy_data, mock_request_exchange_rate):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(user=user, state=POLICY_STATUS_SUBMITTED,
                                                data=json.dumps({'policy_data': policy_data}))
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_INIT,
                                            cost_dollar=(50 * config.DOLLAR_ETH_EXCHANGE_RATE))
    deposit.init_to_wait()
    deposit.save()
    deposit.cost_dollar = (50 * config.DOLLAR_ETH_EXCHANGE_RATE)
    deposit.amount = 50
    deposit.save()
    deposit.wait_to_received()
    deposit.save()
    policy = PolicyApplication.objects.get()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW
