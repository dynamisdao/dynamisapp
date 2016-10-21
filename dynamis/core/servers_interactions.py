import json

import requests
from web3 import Web3, RPCProvider

from dynamis.settings import RPC_PROVIDER_HOST, RPC_PROVIDER_PORT, ETHERSCAN_API_KEY, ETHERSCAN_MAX_RECORDS_TO_RETURN, \
    ETHERSCAN_MAX_PAGES


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


class EtherscanAPIConnector(object):
    def __init__(self):
        self.api_key = ETHERSCAN_API_KEY
        self.url_prefix = 'http://api.etherscan.io/api'
        self.max_records_to_return = ETHERSCAN_MAX_RECORDS_TO_RETURN

    def make_get_request(self, *args, **kwargs):
        params_to_request = {
            'apikey': self.api_key,
            'page': 1,
            'offset': self.max_records_to_return,
            'sort': 'desc'
        }
        if 'page' in kwargs.keys():
            params_to_request.update({'offset': self.max_records_to_return})
        else:
            params_to_request.update({'offset': self.max_records_to_return,
                                      'page': 1})
        params_to_request.update(kwargs)
        return requests.get(self.url_prefix, params_to_request)

    def _search_value_in_api_response_result(self, key, value, **request_kwargs):
        request_kwargs.update({'page': 1})
        attempts = 0
        while attempts <= ETHERSCAN_MAX_PAGES:
            response_content = self.make_get_request(**request_kwargs).content
            content = json.loads(response_content)

            if content['status'] != '1':
                return False

            if value not in response_content:
                attempts += 1
                request_kwargs['page'] += 1
            else:
                for record in content['result']:
                    if record[key] == value:
                        return record

    def get_single_transaction_by_addresses(self, address_from, address_to):
        request_kwargs = {
            'module': 'account',
            'action': 'txlist',
            'address': address_to,
        }

        result = self._search_value_in_api_response_result('from', address_from, **request_kwargs)
        if result:
            return result['hash'], result['value'], result['timeStamp'], result['confirmations']
        else:
            return None, None, None, None
