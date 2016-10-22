import datetime

from constance import config
from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer
from dynamis.apps.payments.models import SmartDeposit, SMART_DEPOSIT_STATUS_WAITING, SMART_DEPOSIT_STATUS_INIT, \
    SMART_DEPOSIT_STATUS_RECEIVED


def test_get_smart_deposit_ok(user_webtest_client, api_client, factories, mock_request_exchange_rate):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=1,
                                            wait_for=datetime.datetime.now() - datetime.timedelta(minutes=5))
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert response.data == SmartDepositShortSerializer(deposit).data


def test_get_smart_deposit_wait_expired(user_webtest_client, api_client, factories, mock_request_exchange_rate):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=1,
                                            wait_for=datetime.datetime.now() - datetime.timedelta(minutes=5))
    deposit = SmartDeposit.objects.get()
    assert deposit.state == 1
    assert deposit.cost == round(deposit.cost_dollar / config.DOLLAR_ETH_EXCHANGE_RATE, 3)

    config.DOLLAR_ETH_EXCHANGE_RATE = 12.686

    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.state == 0
    assert deposit.cost == round(deposit.cost_dollar / 12.686, 3)


def test_send_smart_deposit_ok(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=SMART_DEPOSIT_STATUS_INIT,
                                            cost_dollar=(2 * config.DOLLAR_ETH_EXCHANGE_RATE))
    data_to_send = {
        'amount_in_eth': 2,
        'from_address': 'some_address'
    }

    url = reverse('v1:send-smart-deposit', args=[policy.pk])
    response = api_client.post(url, data_to_send)
    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.from_address == data_to_send['from_address']
    assert deposit.state == SMART_DEPOSIT_STATUS_WAITING


def test_send_smart_deposit_status_wait(user_webtest_client, api_client, factories, mock_refresh_usd_eth_exchange_rate):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=SMART_DEPOSIT_STATUS_INIT,
                                            cost_dollar=(2 * config.DOLLAR_ETH_EXCHANGE_RATE))
    data_to_send = {
        'amount_in_eth': 2,
        'from_address': 'some_address'
    }

    url = reverse('v1:send-smart-deposit', args=[policy.pk])

    deposit.init_to_wait()
    old_deposit_wait_for = deposit.wait_for

    response = api_client.post(url, data_to_send)
    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.wait_for > old_deposit_wait_for
    assert deposit.from_address == data_to_send['from_address']
    assert deposit.state == SMART_DEPOSIT_STATUS_WAITING


def test_send_smart_deposit_status_received(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=SMART_DEPOSIT_STATUS_RECEIVED,
                                            cost_dollar=(2 * config.DOLLAR_ETH_EXCHANGE_RATE))
    data_to_send = {
        'amount_in_eth': 2,
        'from_address': 'some_address'
    }

    url = reverse('v1:send-smart-deposit', args=[policy.pk])

    response = api_client.post(url, data_to_send)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'non_field_errors': 'smart deposit already received'}


def test_send_smart_deposit_less_amount(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=SMART_DEPOSIT_STATUS_INIT,
                                            cost_dollar=(2 * config.DOLLAR_ETH_EXCHANGE_RATE))
    data_to_send = {
        'amount_in_eth': 1.5,
        'from_address': 'some_address'
    }

    url = reverse('v1:send-smart-deposit', args=[policy.pk])
    response = api_client.post(url, data_to_send)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['amount_in_eth'] == ['smart deposit cost is not equal with received amount']
    deposit = SmartDeposit.objects.get()
    assert deposit.from_address is None
    assert deposit.state == SMART_DEPOSIT_STATUS_INIT
