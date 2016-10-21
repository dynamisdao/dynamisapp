import subprocess

import time

from dynamis.apps.payments.business_logic import check_transfers
from dynamis.core.servers_interactions import get_connector_to_rpc_server


def is_rpc_server_running():
    call_code = subprocess.call('ps x | grep testrpc | grep -v grep', shell=True)
    if call_code == 0:
        return True


def setup_module(module):
    if is_rpc_server_running():
        return
    test_rpc_server = subprocess.Popen('testrpc')
    count_to_start = 0
    while count_to_start <= 4 and test_rpc_server.returncode is None:
        time.sleep(2)
        count_to_start += 1


def teardown_module(module):
    if not is_rpc_server_running():
        return
    pid = subprocess.check_output('ps x | grep testrpc | grep -v grep', shell=True).split(' ')[0]
    subprocess.check_call('kill {}'.format(pid), shell=True)


# def test_check_transfers(monkeypatch, mock_rpc_provider):
#     connector = get_connector_to_rpc_server()
#     from_address = connector.eth.coinbase
#     to_address = connector.personal.listAccounts[0]
#     eth_amount = 123
#     transacton_id = connector.personal.signAndSendTransaction(
#         {'to': to_address, 'from': from_address, 'value': eth_amount}, 'the-passphrase')
