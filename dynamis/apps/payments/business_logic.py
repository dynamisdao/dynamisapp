import json

import requests
import time
from django.utils import timezone
from constance import config
from requests import ConnectionError
from rest_framework import status

from dynamis.core.servers_interactions import get_connector_to_rpc_server, EtherscanAPIConnector

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


def check_transfers_change_model_states(wait_tx_model):
    if wait_tx_model.state == wait_tx_model.WAIT_FOR_TX_STATUS_WAITING:
        eth_tx = None

        if wait_tx_model.from_address:
            etherscan = EtherscanAPIConnector()
            eth_tx = etherscan.get_single_transaction_by_addresses(wait_tx_model)

        if eth_tx:
            wait_tx_model.amount = float(eth_tx.eth_value())
            wait_tx_model.eth_tx = eth_tx
            wait_tx_model.save()
            wait_tx_model.wait_to_received()
            wait_tx_model.save()

        elif wait_tx_model.wait_for < timezone.now():
            wait_tx_model.wait_to_init()
            wait_tx_model.save()

    return wait_tx_model


def check_transfers(address_from, address_to):
    connector = get_connector_to_rpc_server()
