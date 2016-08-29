from django.core.urlresolvers import reverse

from dynamis.apps.accounts.api.v1.serializers import AccountConfigSerializer
from dynamis.apps.accounts.models import AccountConfig, User


def test_get_account_config(user_webtest_client, api_client, factories):
    User.objects.update(keybase_username='test_keybase_username')
    account_config = factories.AccountConfigFactory(user=user_webtest_client.user,
                                                    rpc_node_host='http://127.0.0.1:1234')
    url = reverse('v1:account-config-detail', args=[account_config.user.keybase_username])

    page = api_client.get(url)

    assert page.status_code == 200
    assert page.data == AccountConfigSerializer(account_config).data


def test_deny_get_other_user_account_config(api_client, factories):
    other_user = factories.UserFactory(keybase_username='test_keybase_username')
    account_config = factories.AccountConfigFactory(user=other_user)
    url = reverse('v1:account-config-detail', args=[account_config.user.keybase_username])

    page = api_client.get(url)

    assert page.status_code == 404


def test_change_account_config(user_webtest_client, api_client, factories):
    User.objects.update(keybase_username='test_keybase_username')
    new_rpc_node_host = 'http://52.16.72.86:8549'

    account_config = factories.AccountConfigFactory(user=user_webtest_client.user)
    url = reverse('v1:account-config-detail', args=[account_config.user.keybase_username])

    assert AccountConfig.objects.get().rpc_node_host == 'http://localhost:8545'

    page = api_client.put(url, data={'rpc_node_host': new_rpc_node_host})

    assert page.status_code == 200
    assert AccountConfig.objects.get().rpc_node_host == new_rpc_node_host


def test_deny_change_other_user_account_config(api_client, factories):
    new_rpc_node_host = 'http://52.16.72.86:8549'
    other_user = factories.UserFactory(keybase_username='test_keybase_username')

    account_config = factories.AccountConfigFactory(user=other_user)
    url = reverse('v1:account-config-detail', args=[account_config.user.keybase_username])

    assert AccountConfig.objects.get().rpc_node_host == 'http://localhost:8545'

    page = api_client.put(url, data={'rpc_node_host': new_rpc_node_host})

    assert page.status_code == 404
    assert AccountConfig.objects.get().rpc_node_host != new_rpc_node_host
