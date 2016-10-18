import json

import requests
import time
from constance import config
from requests import ConnectionError
from rest_framework import status

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
