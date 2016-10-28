import json

import time
import datetime
import gnupg
import httpretty

import pytest
import web3
from constance import config

from django_webtest import (
    WebTest as BaseWebTest,
    DjangoTestApp as BaseDjangoTestApp,
)

from dynamis.settings import TEST_SYSTEM_ETH_ADDRESS


@pytest.fixture()  # NOQA
def factories(transactional_db):
    import factory

    from factories.accounts import (  # NOQA
        UserFactory
    )
    from factories.policy import (  # NOQA
        PolicyApplicationFactory,
        IdentityApplicationItemFactory,
        EmploymentClaimApplicationItemFactory,
        IdentityPeerReviewFactory,
        EmploymentClaimPeerReviewFactory,
        RiskAssessmentTaskFactory,
    )
    from factories.payments import (
        SmartDepositFactory,
        SmartDepositRefundFactory,
        PremiumPaymentFactory,
        EthAccountFactory,
        TokenAccountFactory,
        EthTxFactory,
        BuyTokenOperationFactory
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.DjangoModelFactory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models_no_db():
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(models_no_db, transactional_db):
    return models_no_db


class DjangoTestApp(BaseDjangoTestApp):
    def _update_environ(self, environ, user):
        user = user or self.user
        return super(DjangoTestApp, self)._update_environ(environ, user)

    @property
    def user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_id = self.session.get('_auth_user_id')
        if user_id:
            return User.objects.get(pk=user_id)
        else:
            return None


class WebTest(BaseWebTest):
    app_class = DjangoTestApp

    def authenticate(self, user):
        self.app.get('/', user=user)

    def unauthenticate(self):
        self.app.get('/', user=None)


@pytest.fixture()  # NOQA
def webtest_client(transactional_db):
    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app


@pytest.fixture()
def user_webtest_client(webtest_client, user):
    web_test = WebTest(methodName='__call__')
    web_test()
    web_test.authenticate(user)
    return web_test.app


@pytest.fixture()  # NOQA
def User(django_user_model):
    """
    A slightly more intuitively named
    `pytest_django.fixtures.django_user_model`
    """
    return django_user_model


@pytest.fixture()
def admin_user(factories, User):
    try:
        return User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        return factories.UserFactory(
            email='admin@example.com',
            is_superuser=True,
            password='password',
        )


@pytest.fixture()
def user(factories, User):
    try:
        return User.objects.get(email='test@example.com')
    except User.DoesNotExist:
        return factories.UserFactory(
            email='test@example.com',
            password='password',
        )


@pytest.fixture()
def user_client(user, client):
    assert client.login(username=user.email, password='password')
    client.user = user
    return client


@pytest.fixture()
def admin_client(admin_user, client):
    assert client.login(username=admin_user.email, password='password')
    client.user = admin_user
    return client


@pytest.fixture()
def api_client(user, db):
    """
    A rest_framework api test client not auth'd.
    """
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    return client


#
#  Identity Verification Stuff
#
@pytest.fixture
def gpg(tmpdir):
    """
    Provides a GPG Keyring that can be used for tests.
    """
    gpg_home = str(tmpdir.mkdir('gpg-home'))
    gpg = gnupg.GPG(gnupghome=gpg_home)
    return gpg


@pytest.fixture
def generate_gpg_key_raw(gpg):
    """
    Function which generates a new key for the gpg keyring
    """

    def _generate_gpg_key_raw():
        seed = gpg.gen_key_input(key_type="RSA", key_length=1024)
        key = gpg.gen_key(seed)
        return key

    return _generate_gpg_key_raw


@pytest.fixture
def gpg_key_raw(generate_gpg_key_raw):
    """
    A gpg key on the gpg keyring
    """
    return generate_gpg_key_raw()


@pytest.fixture
def dummy_public_key_provider(monkeypatch, settings):
    """
    For mocking out the public key provider
    """
    settings.PUBLIC_KEY_PROVIDER_PATH = 'dynamis.utils.testing.DummyPublicKeyProvider'


@pytest.fixture
def generate_gpg_key(dummy_public_key_provider, gpg, monkeypatch,
                     generate_gpg_key_raw):
    """
    Function that generates a GPG key that can be used with the public key
    provider.
    """
    from dynamis.utils import testing

    def _generate_gpg_key(username):
        gpg_key = generate_gpg_key_raw()
        public_key_pem = gpg.export_keys([gpg_key.fingerprint])
        monkeypatch.setitem(testing.KEY_DB, (username,), public_key_pem)
        monkeypatch.setitem(testing.PROOF_DB, (username,), [])
        return gpg_key

    return _generate_gpg_key


@pytest.fixture
def gpg_key(generate_gpg_key):
    """
    Generates a GPG key and includes it in the dummy public key provider's
    database.
    """
    return generate_gpg_key('test')


@pytest.fixture()
def internal_contractor(factories):
    from dynamis.apps.accounts.models import User
    try:
        return User.objects.get(internal_contractor=True)
    except User.DoesNotExist:
        return factories.UserFactory(
            email='internal_contractor@example.com',
            password='password',
            internal_contractor=True
        )


@pytest.fixture
def policy_data():
    policy_data = {
        'identity': {
            "verification_method": "keybase",
            "verification_data": {
                "username": "test",
                "proofs": [],
            },
        },
        'employmentHistory': {
            'jobs': [],
        },
        'questions': {}
    }
    return policy_data


@pytest.fixture()
def mock_rpc_provider(monkeypatch):
    monkeypatch.setattr('dynamis.core.servers_interactions.RPCProvider', web3.TestRPCProvider)


@pytest.fixture()
def mock_call_etherscan_count(monkeypatch):
    monkeypatch.setattr("dynamis.core.servers_interactions.ETHERSCAN_MAX_RECORDS_TO_RETURN", 2)
    monkeypatch.setattr("dynamis.core.servers_interactions.ETHERSCAN_MAX_PAGES", 2)


@pytest.fixture()
def mock_request_get_single_transaction_by_addresses_empty_result(monkeypatch):
    class ResponseMockOk:
        def __init__(self):
            self.status_code = 200
            content_json = {"status": "0", "message": "No transactions found", "result": []}
            self.content = json.dumps(content_json)

        def __call__(self, *args, **kwargs):
            return self

    monkeypatch.setattr("requests.get", ResponseMockOk())


@pytest.fixture()
def mock_refresh_usd_eth_exchange_rate(monkeypatch):
    def pass_func():
        pass

    monkeypatch.setattr('dynamis.apps.payments.models.refresh_usd_eth_exchange_rate', pass_func)


@pytest.fixture()
def mock_request_exchange_rate():
    NEW_ETH_USD_RATE = 12.686
    response = [{
        "id": "ethereum",
        "name": "Ethereum",
        "symbol": "ETH",
        "rank": "1",
        "price_usd": str(NEW_ETH_USD_RATE),
        "price_btc": "0.0196547",
        "24h_volume_usd": "11956600.0",
        "market_cap_usd": "1070934605.0",
        "available_supply": "85090706.0",
        "total_supply": "85090706.0",
        "percent_change_1h": "0.26",
        "percent_change_24h": "5.89",
        "percent_change_7d": "4.83",
        "last_updated": "1476794361"
    }]
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, "http://api.coinmarketcap.com/v1/ticker/ethereum/",
                           body=json.dumps(response),
                           content_type="application/json")


@pytest.fixture()
def mock_request_get_single_transaction_by_addresses():
    tx_time = int(time.mktime((datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).timetuple()))
    response = {"status": "1", "message": "OK", "result":
                [{"blockNumber": "2202431", "timeStamp": "1473064775",
                  "hash": "0xd24d6c937cca54ffde69f059b58cc422c5729dc0d307b6ab892133cc05464e78",
                  "nonce": "286",
                  "blockHash": "0x7f94fed143721aa05448765e72c87ea0df18ef7d2921341f5fb9bf33cbb51ae6",
                  "transactionIndex": "0",
                  "from": "0x5ed8cee6b63b1c6afce3ad7c92f4fd7e1b8fad9f",
                  "to": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                  "value": "0",
                  "gas": "500000", "gasPrice": "100000000000", "isError": "0",
                  "input": "0xb61d27f60000000000000000000000001e549606b695423368e851ff13edef7ea4790fe900000000000000000"
                           "000000000000000000000000000174b1ca8ab05a8c0000000000000000000000000000000000000000000000000"
                           "000000000000000000600000000000000000000000000000000000000000000000000000000000000000",
                  "contractAddress": "", "cumulativeGasUsed": "180885",
                  "gasUsed": "180885",
                  "confirmations": "279470"},
                 {"blockNumber": "2171747", "timeStamp": "1472625374",
                  "hash": "0xdb584b30ab28ecfcdf585c9cf753dbc84a2d4bfa1004fec22cff30559e690a31",
                  "nonce": "5",
                  "blockHash": "0xa6c787d42aabc843caf28cc61fb70dbc9a6cbe1efa9eac3ef4d9b7cb54ab4877",
                  "transactionIndex": "6",
                  "from": "0x00a19cf74a34a349a7a4727cf6435f3daf704de2",
                  "to": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                  "value": "31393856240000000000", "gas": "22444",
                  "gasPrice": "20000000000",
                  "isError": "0", "input": "0x", "contractAddress": "",
                  "cumulativeGasUsed": "260749", "gasUsed": "22444",
                  "confirmations": "310154"},
                 {"blockNumber": "2108601", "timeStamp": "1471722162",
                  "hash": "0x92a88ea2deec2f1b6bc7f678972ffdb2c827a67a29ca8f07a074cf126acbeef1",
                  "nonce": "4",
                  "blockHash": "0x5be5b75b131e1440594c0279e105ad0031376f63c2c8f988ec288b8a29a5b971",
                  "transactionIndex": "25",
                  "from": "0x009a8529fb66b3d434f239a8801492891b48eceb",
                  "to": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                  "value": "34353476240000000000", "gas": "22444",
                  "gasPrice": "20000000000",
                  "isError": "0", "input": "0x", "contractAddress": "",
                  "cumulativeGasUsed": "949445", "gasUsed": "22444",
                  "confirmations": "373300"},
                 {"blockNumber": "2108601", "timeStamp": str(tx_time),
                  "hash": "0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904",
                  "nonce": "4",
                  "blockHash": "0x5be5b75b131e1440594c0279e105ad0031376f63c2c8f988ec288b8a29a5b971",
                  "transactionIndex": "24",
                  "from": "0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                  "to": TEST_SYSTEM_ETH_ADDRESS,
                  "value": "1591000000000000000", "gas": "22444",
                  "gasPrice": "20000000000",
                  "isError": "0", "input": "0x", "contractAddress": "",
                  "cumulativeGasUsed": "927001", "gasUsed": "22444",
                  "confirmations": "373300"},
                 {"blockNumber": "2108601", "timeStamp": str(tx_time),
                  "hash": "0x20f326be6caca6df1073f97595d8aef9826cd41e06a597341dec31d1aa3cb366",
                  "nonce": "4",
                  "blockHash": "0x5be5b75b131e1440594c0279e105ad0031376f63c2c8f988ec288b8a29a5b971",
                  "transactionIndex": "23",
                  "from": "0x0048f63c40c39776d0a79457618e5504a45cb812",
                  "to": TEST_SYSTEM_ETH_ADDRESS,
                  "value": "1600001000000000000", "gas": "22444",
                  "gasPrice": "20000000000",
                  "isError": "0", "input": "0x", "contractAddress": "",
                  "cumulativeGasUsed": "904557", "gasUsed": "22444",
                  "confirmations": "373300"}]}
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, 'http://api.etherscan.io/api',
                           body=json.dumps(response),
                           content_type="application/json")
    httpretty.register_uri(httpretty.GET, 'http://testnet.etherscan.io/api',
                           body=json.dumps(response),
                           content_type="application/json")


@pytest.fixture()
def mock_request_get_single_transaction_by_addresses_less_confirms():
    tx_time = int(time.mktime((datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).timetuple()))
    response = {"status": "1", "message": "OK", "result":
                [
                 {"blockNumber": "2108601", "timeStamp": str(tx_time),
                  "hash": "0x4881e4cd603725595998500085683c0bec29a333c537f96d73fed52967777904",
                  "nonce": "4",
                  "blockHash": "0x5be5b75b131e1440594c0279e105ad0031376f63c2c8f988ec288b8a29a5b971",
                  "transactionIndex": "24",
                  "from": "0x00a6e578bb89ed5aeb9afc699f5ac109681f8c86",
                  "to": TEST_SYSTEM_ETH_ADDRESS,
                  "value": "1591000000000000000", "gas": "22444",
                  "gasPrice": "20000000000",
                  "isError": "0", "input": "0x", "contractAddress": "",
                  "cumulativeGasUsed": "927001", "gasUsed": "22444",
                  "confirmations": str(config.TX_CONFIRMATIONS_COUNT - 1)},
                 {"blockNumber": "2108601",  "timeStamp": str(tx_time),
                  "hash": "0x20f326be6caca6df1073f97595d8aef9826cd41e06a597341dec31d1aa3cb366",
                  "nonce": "4",
                  "blockHash": "0x5be5b75b131e1440594c0279e105ad0031376f63c2c8f988ec288b8a29a5b971",
                  "transactionIndex": "23",
                  "from": "0x0048f63c40c39776d0a79457618e5504a45cb812",
                  "to": TEST_SYSTEM_ETH_ADDRESS,
                  "value": "31447186240000000000", "gas": "22444",
                  "gasPrice": "20000000000",
                  "isError": "0", "input": "0x", "contractAddress": "",
                  "cumulativeGasUsed": "904557", "gasUsed": "22444",
                  "confirmations": str(config.TX_CONFIRMATIONS_COUNT - 1)}]}
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, 'http://api.etherscan.io/api',
                           body=json.dumps(response),
                           content_type="application/json")
    httpretty.register_uri(httpretty.GET, 'http://testnet.etherscan.io/api',
                           body=json.dumps(response),
                           content_type="application/json")


@pytest.fixture()
def mock_call_system_eth_address(monkeypatch):
    monkeypatch.setattr("dynamis.apps.payments.api.v1.views", TEST_SYSTEM_ETH_ADDRESS)

# @pytest.fixture(autouse=True)
# def no_requests(monkeypatch):
#     monkeypatch.delattr("requests.sessions.Session.request")
