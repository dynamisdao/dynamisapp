from web3 import Web3

from dynamis.core.servers_interactions import get_connector_to_rpc_server, EtherscanAPIConnector
from dynamis.settings import RPC_PROVIDER_HOST, TEST_SYSTEM_ETH_ADDRESS
from dynamis.settings import RPC_PROVIDER_PORT


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
                                             mock_call_etherscan_count):
    address_from = "0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86"
    address_to = TEST_SYSTEM_ETH_ADDRESS
    etherscan = EtherscanAPIConnector()
    transaction_id, eth_amount, timestamp, confirmations_count = etherscan.get_single_transaction_by_addresses(
        address_from, address_to)
    assert transaction_id == '0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904'
    assert eth_amount == '33868806240000000000'
    assert timestamp == '1471722162'
    assert confirmations_count == '373300'


def test_get_single_transaction_by_addresses_fake_from(mock_request_get_single_transaction_by_addresses,
                                                       mock_call_etherscan_count):
    address_from = "0x00a6e578bb89ed5aeb9afc699f5ac109681f8c87"
    address_to = TEST_SYSTEM_ETH_ADDRESS
    etherscan = EtherscanAPIConnector()
    transaction_id, eth_amount, timestamp, confirmations_count = etherscan.get_single_transaction_by_addresses(
        address_from, address_to)
    assert transaction_id is None
    assert eth_amount is None
    assert timestamp is None
    assert confirmations_count is None


def test_get_single_transaction_by_addresses_fake_to(mock_request_get_single_transaction_by_addresses_empty_result,
                                                     mock_call_etherscan_count):
    address_from = "0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86"
    address_to = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697baa"
    etherscan = EtherscanAPIConnector()
    transaction_id, eth_amount, timestamp, confirmations_count = etherscan.get_single_transaction_by_addresses(
        address_from, address_to)
    assert transaction_id is None
    assert eth_amount is None
    assert timestamp is None
    assert confirmations_count is None
