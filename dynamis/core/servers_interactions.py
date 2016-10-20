from web3 import Web3, RPCProvider

from dynamis.settings import RPC_PROVIDER_HOST, RPC_PROVIDER_PORT


def get_connector_to_rpc_server(rpc_provider_host=None, rpc_provider_port=None):
    """
    :type rpc_provider_host: str
    :type rpc_provider_port: str
    :rtype: web3.Web3
    """
    if not rpc_provider_host:
        rpc_provider_host = RPC_PROVIDER_HOST
    if not rpc_provider_port:
        rpc_provider_port = RPC_PROVIDER_PORT

    return Web3(RPCProvider(host=rpc_provider_host, port=rpc_provider_port))
