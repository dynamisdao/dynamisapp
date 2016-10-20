from web3 import Web3

from dynamis.core.servers_interactions import get_connector_to_rpc_server
from dynamis.settings import RPC_PROVIDER_HOST
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

