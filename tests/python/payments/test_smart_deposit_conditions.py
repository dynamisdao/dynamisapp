import json

import pytest
from constance import config
from django_fsm import TransitionNotAllowed

from dynamis.apps.payments.models import WAIT_FOR_TX_STATUS_WAITING, WAIT_FOR_TX_STATUS_RECEIVED
from dynamis.apps.policy.models import POLICY_STATUS_SUBMITTED


def test_change_state_to_received(factories, policy_data):
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                data=json.dumps({'policy_data': policy_data}))
    smart_deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                                  cost_dollar=(50 * config.DOLLAR_ETH_EXCHANGE_RATE), amount=50)

    assert smart_deposit.state == WAIT_FOR_TX_STATUS_WAITING
    smart_deposit.wait_to_received()
    assert smart_deposit.state == WAIT_FOR_TX_STATUS_RECEIVED


def test_change_state_to_received_almost_equal(factories, policy_data):
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                data=json.dumps({'policy_data': policy_data}))
    smart_deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                                  cost_dollar=(50.0001 * config.DOLLAR_ETH_EXCHANGE_RATE), amount=50)

    assert smart_deposit.state == WAIT_FOR_TX_STATUS_WAITING
    smart_deposit.wait_to_received()
    assert smart_deposit.state == WAIT_FOR_TX_STATUS_RECEIVED


def test_change_state_to_received_no_amount(factories):
    smart_deposit = factories.SmartDepositFactory(state=WAIT_FOR_TX_STATUS_WAITING, cost_dollar=500)

    assert smart_deposit.state == WAIT_FOR_TX_STATUS_WAITING
    with pytest.raises(TransitionNotAllowed):
        smart_deposit.wait_to_received()

    assert smart_deposit.state == WAIT_FOR_TX_STATUS_WAITING


def test_change_state_to_received_small_amount(factories):
    smart_deposit = factories.SmartDepositFactory(state=WAIT_FOR_TX_STATUS_WAITING, cost_dollar=5000, amount=40)

    assert smart_deposit.state == WAIT_FOR_TX_STATUS_WAITING
    with pytest.raises(TransitionNotAllowed):
        smart_deposit.wait_to_received()

    assert smart_deposit.state == WAIT_FOR_TX_STATUS_WAITING
