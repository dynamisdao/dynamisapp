import json

import datetime

import pytz
import requests
from constance import config
from web3 import Web3, RPCProvider

from dynamis.core.models import EthTransaction
from dynamis.core.utils import datetime_to_timestamp
from dynamis.settings import RPC_PROVIDER_HOST, RPC_PROVIDER_PORT, ETHERSCAN_API_KEY, ETHERSCAN_MAX_RECORDS_TO_RETURN, \
    ETHERSCAN_MAX_PAGES, DEBUG
from dynamis.utils.math import approximately_equal


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
        if DEBUG:
            self.url = 'http://testnet.etherscan.io/api'
        else:
            self.url = 'http://api.etherscan.io/api'
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
        return requests.get(self.url, params_to_request)

    def _search_value_in_api_response_result(self, wait_tx_model, key, value, **request_kwargs):
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
                        if self.check_eth_tx_record(record, wait_tx_model):
                            eth_tx = EthTransaction.objects.create(hash=record['hash'],
                                                                   confirmations=int(record['confirmations']),
                                                                   from_address=wait_tx_model.from_address,
                                                                   to_address=config.SYSTEM_ETH_ADDRESS,
                                                                   value=record['value'],
                                                                   datetime=datetime.datetime.utcfromtimestamp(
                                                                       int(record['timeStamp'])).replace(
                                                                       tzinfo=pytz.utc))
                            return eth_tx
                        else:
                            return

    def check_eth_tx_record(self, record, wait_tx_model):
        wait_from = datetime_to_timestamp(wait_tx_model.created_at)
        wait_to = datetime_to_timestamp(wait_tx_model.wait_for)

        if not wait_from < int(record['timeStamp']) < wait_to:
            print '1'
            return False
        elif EthTransaction.objects.filter(hash=record['hash']).exists():
            print '2-'
            return False
        elif not int(record['confirmations']) >= config.TX_CONFIRMATIONS_COUNT:
            print record['confirmations']
            return False
        elif not approximately_equal(int(record['value']), wait_tx_model.cost_wei,
                                     config.TX_VALUE_DISPERSION):
            print int(record['value']),   wait_tx_model.cost_wei
            print '4'
            return False

        return True

    def get_single_transaction_by_addresses(self, wait_tx_model):
        request_kwargs = {
            'module': 'account',
            'action': 'txlist',
            'address': config.SYSTEM_ETH_ADDRESS,
        }

        eth_tx = self._search_value_in_api_response_result(wait_tx_model, 'from', wait_tx_model.from_address,
                                                           **request_kwargs)
        return eth_tx
