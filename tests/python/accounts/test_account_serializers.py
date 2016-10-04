import datetime

from dynamis.apps.accounts.api.v1.serializers import EthAccountSerializer, AccountShortSerializer, \
    AccountDetailSerializer, AccountListSerializer, AccountLoginResponseSerializer


def test_account_settings_serializer(factories):
    account_settings = factories.EthAccountFactory(eth_address='http://example.com/test_url')

    data = {
        'eth_address': account_settings.eth_address,
    }

    serializer = EthAccountSerializer(account_settings)
    assert serializer.data == data


def test_account_short_serializer(factories):
    user = factories.UserFactory()
    token_account = factories.TokenAccountFactory(user=user)
    eth_account = factories.EthAccountFactory(user=user)

    data = {
        'keybase_username': user.keybase_username,
        'keybase_verified': user.is_keybase_verified,
        'linkedin_account': user.linkedin_account,
        'email': user.email,
        'eth_balance': user.eth_accounts.first().eth_balance,
        'immature_tokens_balance': user.token_account.immature_tokens_balance,
        'mature_tokens_balance': user.token_account.mature_tokens_balance,

    }

    serializer = AccountShortSerializer(user)
    assert serializer.data == data


def test_account_short_serializer_no_eth_and_token_accounts(factories):
    account = factories.UserFactory()

    data = {
        'keybase_username': account.keybase_username,
        'keybase_verified': account.is_keybase_verified,
        'linkedin_account': account.linkedin_account,
        'email': account.email,
        'eth_balance': None,
        'immature_tokens_balance':  None,
        'mature_tokens_balance':  None,

    }

    serializer = AccountShortSerializer(account)
    assert serializer.data == data


def test_account_detail_serializer(factories):
    date_now = datetime.datetime.now()
    account = factories.UserFactory(date_joined=date_now)

    data = {
        'keybase_username': account.keybase_username,
        'keybase_verified': account.is_keybase_verified,
        'email': account.email,
        'date_joined': date_now.isoformat(),
        'last_login': account.last_login,
        'verified_at': account.verified_at,
        'superuser': account.is_superuser,
        'staff': account.is_staff,
        'active': account.is_active,
        'risk_assessor': account.is_risk_assessor,
        'email_verified': False,
        'linkedin_account': account.linkedin_account,
        'id': account.id,
    }

    serializer = AccountDetailSerializer(account)
    assert serializer.data == data


def test_account_list_serializer(factories):
    account = factories.UserFactory()

    data = {
        'keybase_username': account.keybase_username,
        'email': account.email,
        'id': account.id,
    }

    serializer = AccountListSerializer(account)
    assert serializer.data == data


def test_account_login_response_serializer(factories):
    account = factories.UserFactory()

    data = {
        'accountid': account.id,
    }

    serializer = AccountLoginResponseSerializer(account)
    assert serializer.data == data
