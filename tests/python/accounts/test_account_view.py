import datetime

from dateutil.tz import tzlocal
from django.core import mail
from django.core.urlresolvers import reverse
from rest_framework import status

from dynamis.apps.accounts.api.v1.serializers import (AccountShortSerializer, AccountDetailSerializer,
                                                      AccountListSerializer)
from dynamis.apps.accounts.models import User, AccountConfig


def test_get_my_account(user_webtest_client, api_client):
    url = reverse('v1:accounts-detail', args=[user_webtest_client.user.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AccountShortSerializer(user_webtest_client.user).data


def test_get_unauthorized(api_client, factories):
    other_user = factories.UserFactory()
    url = reverse('v1:accounts-detail', args=[other_user.pk])
    api_client.force_authenticate(None)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_other_account_if_admin(api_client, factories):
    other_user = factories.UserFactory()

    user_admin = factories.UserFactory(is_staff=True)
    api_client.force_authenticate(user_admin)

    url = reverse('v1:accounts-detail', args=[other_user.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AccountDetailSerializer(other_user).data


def test_get_other_account_if_not_admin(api_client, factories):
    other_user = factories.UserFactory()

    url = reverse('v1:accounts-detail', args=[other_user.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_my_account(user_webtest_client, api_client):
    new_email = 'test@testemail.com'
    verified_time = datetime.datetime.now(tzlocal())
    User.objects.filter(id=user_webtest_client.user.pk).update(verified_at=verified_time)

    url = reverse('v1:accounts-detail', args=[user_webtest_client.user.pk])

    assert User.objects.get(id=user_webtest_client.user.pk).verified_at == verified_time

    response = api_client.put(url, {'email': new_email})

    assert response.status_code == status.HTTP_200_OK
    assert User.objects.get(id=user_webtest_client.user.pk).email == new_email
    assert User.objects.get(id=user_webtest_client.user.pk).verified_at is None


def test_update_other_account_if_admin(api_client, factories):
    other_user = factories.UserFactory()
    user_admin = factories.UserFactory(is_staff=True)
    api_client.force_authenticate(user_admin)
    assert User.objects.get(id=other_user.pk).is_active is True

    url = reverse('v1:accounts-detail', args=[other_user.pk])

    response = api_client.put(url, {'active': False})

    assert response.status_code == status.HTTP_200_OK
    assert User.objects.get(id=other_user.pk).is_active is False


def test_update_other_account_if_not_admin(api_client, factories):
    new_email = '321@mail.com'
    other_user = factories.UserFactory()

    url = reverse('v1:accounts-detail', args=[other_user.pk])

    response = api_client.put(url, {'email': new_email})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_accounts_if_admin(api_client, factories):
    user_admin = factories.UserFactory(is_staff=True)
    other_user_1 = factories.UserFactory()
    other_user_2 = factories.UserFactory()
    api_client.force_authenticate(user_admin)

    url = reverse('v1:accounts-list')
    response = api_client.get(url)

    assert response.data['count'] == 4
    assert response.data['results'][1] == AccountListSerializer(other_user_1).data
    assert response.status_code == status.HTTP_200_OK


def test_deny_list_accounts_if_not_admin(user_webtest_client, api_client, factories):
    other_user_1 = factories.UserFactory()
    other_user_2 = factories.UserFactory()

    url = reverse('v1:accounts-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_list_unauthorized(api_client, factories):
    other_user = factories.UserFactory()
    url = reverse('v1:accounts-list')
    api_client.force_authenticate(None)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_account(api_client, factories):
    email = 'test@email.com'
    password = 'test_pass'
    keybase_username = 'test_keybase'
    eth_address = 'http://example.com/123'
    data = {
        'email': email,
        'password1': password,
        'password2': password,
        'keybase_username': keybase_username,
        'eth_address': eth_address
    }
    url = reverse('v1:accounts-list')
    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(email=email, keybase_username=keybase_username)
    assert user.is_keybase_verified is False
    account_config = AccountConfig.objects.get(user=user)
    assert account_config.rpc_node_host == eth_address


def test_user_creation_api_view(User, api_client):
    account_create_url = reverse('v1:accounts-list')
    test_email = 'test-1@example.com'

    mail.outbox = []

    assert not User.objects.filter(email='test-1@example.com').exists()

    assert len(mail.outbox) == 0

    data = {
        'email': test_email,
        'password1': 'test-password',
        'password2': 'test-password',
    }

    # ensure we aren't already authenticated
    assert '_auth_user_id' not in api_client.session.keys()

    response = api_client.post(account_create_url, data)
    assert response.status_code == status.HTTP_201_CREATED, response.data

    # Make sure verification email was sent.
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to[0] == test_email

    assert User.objects.filter(email=test_email).exists()

    # see that we were logged in.
    assert '_auth_user_id' in api_client.session.keys()


def test_user_creation_debug_no_verify_api_view(User, api_client):
    account_create_url = reverse('v1:accounts-list')
    test_email = 'test-1@example.com'

    mail.outbox = []

    assert not User.objects.filter(email='test-1@example.com').exists()

    assert len(mail.outbox) == 0

    data = {
        'email': test_email,
        'password1': 'test-password',
        'password2': 'test-password',
        'debug_no_verify': True
    }

    # ensure we aren't already authenticated
    assert '_auth_user_id' not in api_client.session.keys()

    response = api_client.post(account_create_url, data)
    assert response.status_code == status.HTTP_201_CREATED, response.data

    # Make sure verification email was sent.
    assert len(mail.outbox) == 0

    assert User.objects.filter(email=test_email, verified_at__isnull=False).exists()

    # see that we were logged in.
    assert '_auth_user_id' in api_client.session.keys()
