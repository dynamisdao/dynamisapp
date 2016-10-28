from constance import config
from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import status

from dynamis.apps.payments.api.v1.serializers import TokenAccountShortSerializer
from dynamis.apps.payments.models import WAIT_FOR_TX_STATUS_WAITING, WAIT_FOR_TX_STATUS_INIT, \
    WAIT_FOR_TX_STATUS_RECEIVED, BuyTokenOperation
from dynamis.core.models import EthTransaction
from dynamis.utils.math import approximately_equal


def test_get_immature_tokens_info_not_assessor(user_webtest_client, api_client, factories,
                                               mock_request_exchange_rate,
                                               mock_request_get_single_transaction_by_addresses,
                                               mock_call_system_eth_address):
    eth_tx = factories.EthTxFactory()
    token_account = factories.TokenAccountFactory(user=user_webtest_client.user)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account, eth_tx=eth_tx,
                                                             state=WAIT_FOR_TX_STATUS_RECEIVED,
                                                             wait_for=timezone.now() - timezone.timedelta(days=15),
                                                             from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86")
    url = reverse('v1:immature-tokens-info', args=[user_webtest_client.user.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {'detail': 'Access not allowed.'}


def test_get_immature_tokens_info_ok_status_received(user_webtest_client, api_client, factories,
                                                     mock_request_exchange_rate,
                                                     mock_request_get_single_transaction_by_addresses,
                                                     mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    eth_tx = factories.EthTxFactory()
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account, eth_tx=eth_tx,
                                                             state=WAIT_FOR_TX_STATUS_RECEIVED,
                                                             wait_for=timezone.now() - timezone.timedelta(days=15),
                                                             from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    eth_tx = EthTransaction.objects.get()
    buy_token_operation = BuyTokenOperation.objects.get(eth_tx=eth_tx)
    assert buy_token_operation.amount is None
    assert buy_token_operation.eth_tx.hash == eth_tx.hash
    assert response.data == TokenAccountShortSerializer(token_account).data


def test_get_immature_tokens_ok_status_init(user_webtest_client, api_client, factories,
                                            mock_request_exchange_rate,
                                            mock_request_get_single_transaction_by_addresses,
                                            mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_INIT,
                                                             wait_for=timezone.now() - timezone.timedelta(days=15),
                                                             from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    buy_token_operation = BuyTokenOperation.objects.get()
    assert buy_token_operation.amount is None
    assert buy_token_operation.eth_tx is None
    assert response.data == TokenAccountShortSerializer(token_account).data


def test_get_immature_tokens_ok_status_wait_almost_equal_plus(user_webtest_client, api_client, factories,
                                                              mock_request_exchange_rate,
                                                              mock_request_get_single_transaction_by_addresses,
                                                              mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_WAITING,
                                                             count=16,
                                                             wait_for=timezone.now() + timezone.timedelta(minutes=5),
                                                             from_address="0x0048f63c40c39776d0a79457618e5504a45cb812")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    eth_tx = EthTransaction.objects.get()
    buy_token_operation = BuyTokenOperation.objects.get(eth_tx=eth_tx)
    assert approximately_equal(buy_token_operation.amount, buy_token_operation.count * config.EHT_TOKEN_EXCHANGE_RATE,
                               config.TX_VALUE_DISPERSION)
    assert buy_token_operation.state == WAIT_FOR_TX_STATUS_RECEIVED
    assert buy_token_operation.eth_tx.hash == '0x20f326be6caca6df1073f97595d8aef9826cd41e06a597341dec31d1aa3cb366'
    assert response.data == TokenAccountShortSerializer(token_account).data


def test_get_immature_tokens_wait_expired(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                          mock_request_get_single_transaction_by_addresses,
                                          mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_WAITING,
                                                             count=16,
                                                             wait_for=timezone.now() - timezone.timedelta(minutes=5),
                                                             from_address="0x0048f63c40c39776d0a79457618e5504a45cb812")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    buy_token_operation = BuyTokenOperation.objects.get()
    assert buy_token_operation.amount is None
    assert buy_token_operation.eth_tx is None
    assert buy_token_operation.state == WAIT_FOR_TX_STATUS_INIT


def test_get_immature_tokens_tx_exists(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                       mock_request_get_single_transaction_by_addresses,
                                       mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    eth_tx = factories.EthTxFactory(hash='0x20f326be6caca6df1073f97595d8aef9826cd41e06a597341dec31d1aa3cb366')
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_WAITING,
                                                             count=16,
                                                             wait_for=timezone.now() + timezone.timedelta(minutes=5),
                                                             from_address="0x0048f63c40c39776d0a79457618e5504a45cb812")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    buy_token_operation = BuyTokenOperation.objects.get()
    assert buy_token_operation.amount is None
    assert buy_token_operation.eth_tx is None
    assert buy_token_operation.state == WAIT_FOR_TX_STATUS_WAITING


def test_get_immature_tokens_less_amount(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                         mock_request_get_single_transaction_by_addresses,
                                         mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_WAITING,
                                                             count=20,
                                                             wait_for=timezone.now() + timezone.timedelta(minutes=5),
                                                             from_address="0x0048f63c40c39776d0a79457618e5504a45cb812")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    buy_token_operation = BuyTokenOperation.objects.get()
    assert buy_token_operation.amount is None
    assert buy_token_operation.eth_tx is None
    assert buy_token_operation.state == WAIT_FOR_TX_STATUS_WAITING


def test_get_immature_tokens_less_confirms(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                           mock_request_get_single_transaction_by_addresses_less_confirms,
                                           mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_WAITING,
                                                             count=16,
                                                             wait_for=timezone.now() + timezone.timedelta(minutes=5),
                                                             from_address="0x0048f63c40c39776d0a79457618e5504a45cb812")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    buy_token_operation = BuyTokenOperation.objects.get()
    assert buy_token_operation.amount is None
    assert buy_token_operation.eth_tx is None
    assert buy_token_operation.state == WAIT_FOR_TX_STATUS_WAITING


def test_get_immature_tokens_fake_from_address(user_webtest_client, api_client, factories, mock_request_exchange_rate,
                                               mock_request_get_single_transaction_by_addresses,
                                               mock_call_system_eth_address):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_WAITING,
                                                             count=16,
                                                             wait_for=timezone.now() + timezone.timedelta(minutes=5),
                                                             from_address="0x0048f63c40c39777d0a79457618e5504a45cb813")
    url = reverse('v1:immature-tokens-info', args=[user_assessor.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    buy_token_operation = BuyTokenOperation.objects.get()
    assert buy_token_operation.amount is None
    assert buy_token_operation.eth_tx is None
    assert buy_token_operation.state == WAIT_FOR_TX_STATUS_WAITING


def test_buy_immature_tokens_ok(user_webtest_client, api_client, factories):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    data_to_send = {
        'count': 22,
        'from_address': 'some_address'
    }
    url = reverse('v1:buy-immature-tokens', args=[user_assessor.pk])
    response = api_client.post(url, data_to_send)
    assert response.status_code == status.HTTP_200_OK
    buy_token_operation = BuyTokenOperation.objects.get()
    assert buy_token_operation.eth_tx is None
    assert buy_token_operation.count == 22
    assert buy_token_operation.from_address == data_to_send['from_address']
    assert buy_token_operation.state == WAIT_FOR_TX_STATUS_WAITING


def test_buy_immature_tokens_already_wait(user_webtest_client, api_client, factories):
    user_assessor = factories.UserFactory(is_risk_assessor=True)
    api_client.force_authenticate(user_assessor)
    token_account = factories.TokenAccountFactory(user=user_assessor)
    buy_token_operation = factories.BuyTokenOperationFactory(token_account=token_account,
                                                             state=WAIT_FOR_TX_STATUS_WAITING,
                                                             count=16,
                                                             wait_for=timezone.now() + timezone.timedelta(minutes=5),
                                                             from_address="0x0048f63c40c39777d0a79457618e5504a45cb813")
    data_to_send = {
        'count': 22,
        'from_address': 'some_address'
    }

    url = reverse('v1:buy-immature-tokens', args=[user_assessor.pk])
    response = api_client.post(url, data_to_send)
    assert response.data == {'non_field_errors': 'you try to buy token second time, we still wait for previous payment'}
    assert response.status_code == status.HTTP_400_BAD_REQUEST
