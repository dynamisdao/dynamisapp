import datetime

from constance import config
from web3 import Web3

from django.utils import timezone

from dynamis.apps.payments.models import WAIT_FOR_TX_STATUS_WAITING
from dynamis.core.servers_interactions import get_connector_to_rpc_server, EtherscanAPIConnector
from dynamis.settings import RPC_PROVIDER_HOST, TEST_SYSTEM_ETH_ADDRESS
from dynamis.settings import RPC_PROVIDER_PORT
from dynamis.utils.math import approximately_equal


def test_get_connector_to_rpc_server():
    host = 'test_host'
    port = '9999'
    connector = get_connector_to_rpc_server(host, port)
    assert isinstance(connector, Web3)
    assert connector.currentProvider.host == host
    assert connector.currentProvider.port == int(port)


def test_get_connector_to_rpc_server_defaults():
    connector = get_connector_to_rpc_server()
    assert isinstance(connector, Web3)
    assert connector.currentProvider.host == RPC_PROVIDER_HOST
    assert connector.currentProvider.port == int(RPC_PROVIDER_PORT)


def test_get_single_transaction_by_addresses(mock_request_get_single_transaction_by_addresses,
                                             mock_call_etherscan_count, mock_request_exchange_rate, factories):
    address_to = TEST_SYSTEM_ETH_ADDRESS
    etherscan = EtherscanAPIConnector()
    wait_for = timezone.now() + datetime.timedelta(minutes=5)
    deposit = factories.SmartDepositFactory(state=WAIT_FOR_TX_STATUS_WAITING,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                                            wait_for=wait_for)
    eth_tx = etherscan.get_single_transaction_by_addresses(deposit)
    assert eth_tx.hash == '0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904'
    assert eth_tx.value == '1591000000000000000'
    assert approximately_equal(eth_tx.eth_value(), 1.591, config.TX_VALUE_DISPERSION) is True
    assert eth_tx.datetime < wait_for
    assert eth_tx.confirmations == 373300


def test_get_single_transaction_by_addresses_fake_from(mock_request_get_single_transaction_by_addresses,
                                                       mock_call_etherscan_count, factories):
    address_from = "0x00a6e578bb89ed5aeb9afc699f5ac109681f8c87"
    address_to = TEST_SYSTEM_ETH_ADDRESS
    etherscan = EtherscanAPIConnector()
    wait_for = timezone.now() + datetime.timedelta(minutes=5)
    deposit = factories.SmartDepositFactory(state=WAIT_FOR_TX_STATUS_WAITING,
                                            from_address="0x00a6e578bb89ed5aeb9afc699f5ac109681f8c87",
                                            wait_for=wait_for)
    eth_tx = etherscan.get_single_transaction_by_addresses(deposit)
    assert eth_tx is None
