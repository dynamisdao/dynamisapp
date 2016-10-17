from django.core.urlresolvers import reverse

from dynamis.apps.accounts.api.v1.serializers import EthAccountSerializer
from dynamis.apps.payments.models import EthAccount


def test_get_account_config(user_webtest_client, api_client, factories):
    account_config = factories.EthAccountFactory(user=user_webtest_client.user,
                                                    eth_address='http://127.0.0.1:1234')
    url = reverse('v1:account-settings-detail', args=[account_config.pk])

    page = api_client.get(url)

    assert page.status_code == 200
    assert page.data == EthAccountSerializer(account_config).data


def test_deny_get_other_user_account_config(api_client, factories):
    account_config = factories.EthAccountFactory()
    url = reverse('v1:account-settings-detail', args=[account_config.user.pk])

    page = api_client.get(url)

    assert page.status_code == 404


def test_change_account_config(user_webtest_client, api_client, factories):
    new_eth_address = 'http://52.16.72.86:8549'

    account_config = factories.EthAccountFactory(user=user_webtest_client.user)
    url = reverse('v1:account-settings-detail', args=[account_config.pk])

    assert EthAccount.objects.get().eth_node_host is None

    page = api_client.put(url, data={'eth_node_host': new_eth_address})

    assert page.status_code == 200
    assert EthAccount.objects.get().eth_node_host == new_eth_address


def test_deny_change_other_user_account_config(api_client, factories):
    new_eth_address = 'http://52.16.72.86:8549'
    other_user = factories.UserFactory()

    account_config = factories.EthAccountFactory(user=other_user)
    url = reverse('v1:account-settings-detail', args=[account_config.pk])

    assert EthAccount.objects.get().eth_address is None

    page = api_client.put(url, data={'eth_address': new_eth_address})

    assert page.status_code == 404
    assert EthAccount.objects.get().eth_address != new_eth_address
