import json

import datetime

import pytz
import requests
import time
from django.utils import timezone
from constance import config
from requests import ConnectionError
from rest_framework import status

from dynamis.core.servers_interactions import get_connector_to_rpc_server, EtherscanAPIConnector
from dynamis.utils.math import approximately_equal

EXCHANGE_RATE_URL = 'http://api.coinmarketcap.com/v1/ticker/ethereum/'


def _perform_request():
    response = requests.get(EXCHANGE_RATE_URL)
    if response.status_code != status.HTTP_200_OK:
        raise ConnectionError
    return response


def refresh_usd_eth_exchange_rate():
    try:
        response = _perform_request()
    except ConnectionError:
        time.sleep(2)
        response = _perform_request()
    response_json = json.loads(response.content)
    assert response_json[0]['id'] == "ethereum"
    config.DOLLAR_ETH_EXCHANGE_RATE = round(float(response_json[0]['price_usd']), 3)
    

def check_transfers_change_smart_deposit_states(smart_deposit):
    # TODO change to variable
    if smart_deposit.state == 1:
        tx_hash, tx_value, tx_timestamp, tx_confirmations = None, None, None, None
        if smart_deposit.from_address:
            etherscan = EtherscanAPIConnector()
            tx_hash, tx_value, tx_timestamp, tx_confirmations = \
                etherscan.get_single_transaction_by_addresses(smart_deposit.from_address, config.SYSTEM_ETH_ADDRESS)

            if tx_timestamp:
                time_to_check = datetime.datetime.utcfromtimestamp(int(tx_timestamp)).replace(tzinfo=pytz.utc)
            else:
                time_to_check = timezone.now()
        else:
            time_to_check = timezone.now()

        if smart_deposit.wait_for < time_to_check:
            smart_deposit.wait_to_init()
            smart_deposit.cost_dollar = smart_deposit.cost * config.DOLLAR_ETH_EXCHANGE_RATE
            smart_deposit.save()

        elif tx_hash and int(tx_confirmations) >= config.TX_CONFIRMATIONS_COUNT \
                and approximately_equal(float(tx_value), smart_deposit.cost, config.TX_VALUE_DISPERSION):
            smart_deposit.amount = float(tx_value)
            smart_deposit.tx_hash = tx_hash
            smart_deposit.save()
            smart_deposit.wait_to_received()
            smart_deposit.save()

    return smart_deposit
            
        


def check_transfers(address_from, address_to):
    connector = get_connector_to_rpc_server()