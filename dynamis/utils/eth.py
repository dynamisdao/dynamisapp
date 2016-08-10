import os
import sys
import socket
import json
import contextlib
import io
import time


def get_default_ipc_path():
    if sys.platform == 'darwin':
        ipc_path = os.path.expanduser("~/Library/Ethereum/geth.ipc")
    elif sys.platform == 'linux2':
        ipc_path = os.path.expanduser("~/.ethereum/geth.ipc")
    elif sys.platform == 'win32':
        ipc_path = os.path.expanduser("\\~\\AppData\\Roaming\\Ethereum")
    else:
        raise ValueError(
            "Unsupported platform.  Only darwin/linux2/win32 are "
            "supported.  You must specify the ipc_path"
        )
    return ipc_path


def get_ipc_socket(ipc_path=None):
    if ipc_path is None:
        ipc_path = get_default_ipc_path()

    if not os.path.exists(ipc_path):
        raise OSError("No ipc socket found at: `{0}`".format(ipc_path))

    _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    _socket.connect(ipc_path)
    # Tell the socket not to block on reads.
    _socket.settimeout(0.2)
    return _socket


def send_ipc_request(request, timeout=3):
    with contextlib.closing(get_ipc_socket()) as ipc_socket:
        ipc_socket.sendall(request)
        buffer = io.BytesIO()
        start = time.time()

        while time.time() < start + timeout:
            while True:
                try:
                    buffer.write(ipc_socket.recv(4096))
                except socket.timeout:
                    break

            try:
                response = json.loads(buffer.getvalue())
                break
            except ValueError:
                continue
        else:
            raise ValueError("Timeout waiting for IPC response")

    if "error" in response:
        raise ValueError(response["error"]["message"])

    return response


_nonce = 0


def get_nonce():
    global _nonce
    nonce = _nonce
    _nonce += 1
    return nonce


def construct_json_request(method, params):
    request = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": get_nonce(),
    })
    return request


def get_transaction_params(_from=None, to=None, gas=None, gas_price=None,
                           value=0, data=None):
    params = {}

    if _from is None:
        raise ValueError("You must specify ")

    params['from'] = _from

    if to is None and data is None:
        raise ValueError("A `to` address is only optional for contract creation")
    elif to is not None:
        params['to'] = to

    if gas is not None:
        params['gas'] = hex(gas)

    if gas_price is not None:
        params['gasPrice'] = hex(gas_price)

    if value is not None:
        params['value'] = hex(value).rstrip('L')

    if data is not None:
        params['data'] = data

    return params


def send_transaction(_from=None, to=None, gas=None, gas_price=None,
                     value=0, data=None):
    """
    https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sendtransaction
    """
    params = get_transaction_params(_from, to, gas, gas_price, value, data)

    request = construct_json_request("eth_sendTransaction", [params])
    response = send_ipc_request(request)

    return response['result']


def unlock_account(address, password, timeout_seconds=10):
    """
    https://github.com/ethereum/go-ethereum/wiki/JavaScript-Console#personalunlockaccount
    """
    request = construct_json_request(
        'personal_unlockAccount',
        [address, password, timeout_seconds],
    )
    response = send_ipc_request(request)
    return response['result']
