import pytest
from django_fsm import TransitionNotAllowed

from dynamis.apps.payments.models import SMART_DEPOSIT_STATUS_WAITING, SMART_DEPOSIT_STATUS_RECEIVED


def test_change_state_to_received(factories):
    smart_deposit = factories.SmartDepositFactory(state=SMART_DEPOSIT_STATUS_WAITING, coast_dollar=50, amount=50)

    assert smart_deposit.state == SMART_DEPOSIT_STATUS_WAITING
    smart_deposit.wait_to_received()
    assert smart_deposit.state == SMART_DEPOSIT_STATUS_RECEIVED


def test_change_state_to_received_no_amount(factories):
    smart_deposit = factories.SmartDepositFactory(state=SMART_DEPOSIT_STATUS_WAITING, coast_dollar=500)

    assert smart_deposit.state == SMART_DEPOSIT_STATUS_WAITING
    with pytest.raises(TransitionNotAllowed):
        smart_deposit.wait_to_received()

    assert smart_deposit.state == SMART_DEPOSIT_STATUS_WAITING


def test_change_state_to_received_small_amount(factories):
    smart_deposit = factories.SmartDepositFactory(state=SMART_DEPOSIT_STATUS_WAITING, coast_dollar=5000, amount=40)

    assert smart_deposit.state == SMART_DEPOSIT_STATUS_WAITING
    with pytest.raises(TransitionNotAllowed):
        smart_deposit.wait_to_received()

    assert smart_deposit.state == SMART_DEPOSIT_STATUS_WAITING
