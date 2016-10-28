import datetime
import json

import pytz
from constance import config
from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import status

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer
from dynamis.apps.payments.models import SmartDeposit, WAIT_FOR_TX_STATUS_WAITING, WAIT_FOR_TX_STATUS_INIT, \
    WAIT_FOR_TX_STATUS_RECEIVED
from dynamis.apps.policy.models import POLICY_STATUS_SUBMITTED
from dynamis.core.models import EthTransaction
from dynamis.utils.math import approximately_equal


def test_get_smart_deposit_ok_status_received(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                              mock_request_get_single_transaction_by_addresses,
                                              mock_call_system_eth_address):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    eth_tx = factories.EthTxFactory()
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_RECEIVED,
                                            wait_for=timezone.now() - timezone.timedelta(days=15),
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            eth_tx=eth_tx)
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    eth_tx = EthTransaction.objects.get()
    deposit = SmartDeposit.objects.get(eth_tx=eth_tx)
    assert deposit.amount == 0
    assert deposit.eth_tx.hash == eth_tx.hash
    assert response.data == SmartDepositShortSerializer(deposit).data


def test_get_smart_deposit_ok_status_init(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                          mock_request_get_single_transaction_by_addresses,
                                          mock_call_system_eth_address):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_INIT,
                                            wait_for=timezone.now() + timezone.timedelta(minutes=15))
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.amount == 0
    assert deposit.eth_tx is None
    assert response.data == SmartDepositShortSerializer(deposit).data


def test_get_smart_deposit_ok_status_wait(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                          mock_request_get_single_transaction_by_addresses,
                                          mock_call_system_eth_address, policy_data):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user, state=POLICY_STATUS_SUBMITTED,
                                                data=json.dumps({'policy_data': policy_data}))
    wait_for = datetime.datetime.now() + datetime.timedelta(minutes=5)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            wait_for=wait_for,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            cost_dollar=(1.591 * config.DOLLAR_ETH_EXCHANGE_RATE))
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    eth_tx = EthTransaction.objects.get()
    deposit = SmartDeposit.objects.get(eth_tx=eth_tx)
    assert approximately_equal(deposit.amount, 1.591, config.TX_VALUE_DISPERSION)
    assert deposit.state == WAIT_FOR_TX_STATUS_RECEIVED
    assert deposit.eth_tx.hash == '0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904'
    assert response.data == SmartDepositShortSerializer(deposit).data


def test_get_smart_deposit_ok_status_wait_almost_equal_minus(user_webtest_client, api_client, factories,
                                                             mock_request_exchange_rate,
                                                             mock_request_get_single_transaction_by_addresses,
                                                             mock_call_system_eth_address, policy_data):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user, state=POLICY_STATUS_SUBMITTED,
                                                data=json.dumps({'policy_data': policy_data}))
    wait_for = datetime.datetime.now() + datetime.timedelta(minutes=5)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            wait_for=wait_for,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            cost_dollar=(1.591 * config.DOLLAR_ETH_EXCHANGE_RATE - 0.0001))
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    eth_tx = EthTransaction.objects.get()
    deposit = SmartDeposit.objects.get(eth_tx=eth_tx)
    assert deposit.state == WAIT_FOR_TX_STATUS_RECEIVED
    assert approximately_equal(deposit.amount, 1.591, config.TX_VALUE_DISPERSION)
    assert deposit.eth_tx.hash == '0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904'
    assert response.data == SmartDepositShortSerializer(deposit).data


def test_get_smart_deposit_ok_status_wait_almost_equal_plus(user_webtest_client, api_client, factories,
                                                            mock_request_exchange_rate,
                                                            mock_request_get_single_transaction_by_addresses,
                                                            mock_call_system_eth_address, policy_data):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user, state=POLICY_STATUS_SUBMITTED,
                                                data=json.dumps({'policy_data': policy_data}))
    wait_for = datetime.datetime.now() + datetime.timedelta(minutes=5)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            wait_for=wait_for,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            cost_dollar=(1.591 * config.DOLLAR_ETH_EXCHANGE_RATE + 0.0001))
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    eth_tx = EthTransaction.objects.get()
    deposit = SmartDeposit.objects.get(eth_tx=eth_tx)
    assert deposit.state == WAIT_FOR_TX_STATUS_RECEIVED
    assert approximately_equal(deposit.amount, 1.591, config.TX_VALUE_DISPERSION)
    assert deposit.eth_tx.hash == '0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904'
    assert response.data == SmartDepositShortSerializer(deposit).data


def test_get_smart_deposit_wait_expired(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                        mock_request_get_single_transaction_by_addresses,
                                        mock_call_system_eth_address):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            wait_for=timezone.datetime.now() - timezone.timedelta(minutes=5),
                                            cost_dollar=(1.591 * config.DOLLAR_ETH_EXCHANGE_RATE))
    deposit = SmartDeposit.objects.get()
    assert deposit.state == 1
    assert deposit.cost == round(deposit.cost_dollar / config.DOLLAR_ETH_EXCHANGE_RATE, 3)

    config.DOLLAR_ETH_EXCHANGE_RATE = 12.686

    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.amount == 0
    assert deposit.eth_tx is None
    assert deposit.state == WAIT_FOR_TX_STATUS_INIT
    assert deposit.cost == round(deposit.cost_dollar / 12.686, 3)


def test_get_smart_deposit_wait_expired_from_address(user_webtest_client, api_client, factories,
                                                     mock_request_exchange_rate,
                                                     mock_request_get_single_transaction_by_addresses,
                                                     mock_call_system_eth_address):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)

    wait_for = datetime.datetime.now() - datetime.timedelta(minutes=5)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            wait_for=wait_for)
    deposit = SmartDeposit.objects.get()
    assert deposit.state == 1

    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.amount == 0
    assert deposit.eth_tx is None
    assert deposit.state == WAIT_FOR_TX_STATUS_INIT


def test_get_smart_deposit_less_amount(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                        mock_request_get_single_transaction_by_addresses,
                                        mock_call_system_eth_address):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            wait_for=timezone.datetime.now() + timezone.timedelta(minutes=5),
                                            cost_dollar=(2.591 * config.DOLLAR_ETH_EXCHANGE_RATE))
    deposit = SmartDeposit.objects.get()
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.amount == 0
    assert deposit.eth_tx is None
    assert deposit.state == WAIT_FOR_TX_STATUS_WAITING


def test_get_smart_deposit_less_confirms(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                         mock_request_get_single_transaction_by_addresses_less_confirms,
                                        mock_call_system_eth_address):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            wait_for=timezone.datetime.now() + timezone.timedelta(minutes=5),
                                            cost_dollar=(1.591 * config.DOLLAR_ETH_EXCHANGE_RATE))
    deposit = SmartDeposit.objects.get()
    assert deposit.state == 1
    assert deposit.cost == round(deposit.cost_dollar / config.DOLLAR_ETH_EXCHANGE_RATE, 3)

    config.DOLLAR_ETH_EXCHANGE_RATE = 12.686

    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.amount == 0
    assert deposit.eth_tx is None
    assert deposit.state == WAIT_FOR_TX_STATUS_WAITING


def test_get_smart_deposit_fake_from_address(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                             mock_request_get_single_transaction_by_addresses,
                                             mock_call_system_eth_address):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    # wait_for = datetime.datetime.utcfromtimestamp(1471722162).replace(tzinfo=pytz.utc) - datetime.timedelta(minutes=5)
    wait_for = datetime.datetime.now() + datetime.timedelta(minutes=5)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_WAITING,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5bc109681f8c96",
                                            wait_for=wait_for)
    deposit = SmartDeposit.objects.get()
    assert deposit.state == 1

    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.amount == 0
    assert deposit.eth_tx is None
    assert deposit.state == WAIT_FOR_TX_STATUS_WAITING


def test_send_smart_deposit_ok(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_INIT,
                                            cost_dollar=(2 * config.DOLLAR_ETH_EXCHANGE_RATE))
    data_to_send = {
        'amount_in_eth': 2,
        'from_address': 'some_address'
    }

    url = reverse('v1:send-smart-deposit', args=[policy.pk])
    response = api_client.post(url, data_to_send)
    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.eth_tx is None
    assert deposit.from_address == data_to_send['from_address']
    assert deposit.state == WAIT_FOR_TX_STATUS_WAITING


def test_send_smart_deposit_status_wait(user_webtest_client, api_client, factories, mock_refresh_usd_eth_exchange_rate):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_INIT,
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
    assert deposit.eth_tx is None
    assert deposit.from_address == data_to_send['from_address']
    assert deposit.state == WAIT_FOR_TX_STATUS_WAITING


def test_send_smart_deposit_status_received(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_RECEIVED,
                                            cost_dollar=(2 * config.DOLLAR_ETH_EXCHANGE_RATE))
    data_to_send = {
        'amount_in_eth': 2,
        'from_address': 'some_address'
    }

    url = reverse('v1:send-smart-deposit', args=[policy.pk])

    response = api_client.post(url, data_to_send)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'non_field_errors': 'smart deposit already received'}
    deposit = SmartDeposit.objects.get()
    assert deposit.state == WAIT_FOR_TX_STATUS_RECEIVED


def test_send_smart_deposit_less_amount(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_INIT,
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
    assert deposit.eth_tx is None
    assert deposit.from_address is None
    assert deposit.state == WAIT_FOR_TX_STATUS_INIT
