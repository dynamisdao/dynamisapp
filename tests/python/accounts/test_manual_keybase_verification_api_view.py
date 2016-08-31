from django.core import signing
from django.core.urlresolvers import reverse

from rest_framework import status


# TODO - deprecated
def test_manual_keybase_verification_DEPR(api_client, user, gpg_key, gpg, factories):
    keybase_verify_url = reverse('v1:verify-keybase')

    token = signing.dumps(user.pk)

    assert user.keybase_username == ''

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(token).data,
    }

    response = api_client.put(keybase_verify_url, data=data)
    assert response.status_code == status.HTTP_200_OK, response.data

    user.refresh_from_db()
    assert user.keybase_username == 'test'


def test_manual_keybase_verification_ok(api_client, user, gpg_key, gpg, factories):
    keybase_verify_url = reverse('v1:verify-keybase-detail', args=[user.pk])

    token = signing.dumps(user.pk)

    assert user.keybase_username == ''
    assert user.is_keybase_verified is False

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(token).data,
    }

    response = api_client.put(keybase_verify_url, data=data)
    assert response.status_code == status.HTTP_200_OK, response.data

    user.refresh_from_db()
    assert user.keybase_username == 'test'
    assert user.is_keybase_verified is True


def test_manual_keybase_verification_deny(api_client, user, gpg_key, gpg, factories):
    new_user = factories.UserFactory()
    keybase_verify_url = reverse('v1:verify-keybase-detail', args=[new_user.pk])

    token = signing.dumps(new_user.pk)

    assert new_user.keybase_username == ''
    assert user.is_keybase_verified is False

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(token).data,
    }

    response = api_client.put(keybase_verify_url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response.data

    new_user.refresh_from_db()
    assert new_user.keybase_username == ''
    assert user.is_keybase_verified is False


def test_manual_keybase_verification_ok_admin(api_client, user, gpg_key, gpg, factories):
    keybase_verify_url = reverse('v1:verify-keybase-detail', args=[user.pk])
    user_admin = factories.UserFactory(is_staff=True)
    api_client.force_authenticate(user_admin)

    token = signing.dumps(user.pk)

    assert user.keybase_username == ''
    assert user.is_keybase_verified is False

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(token).data,
    }

    response = api_client.put(keybase_verify_url, data=data)
    assert response.status_code == status.HTTP_200_OK, response.data

    user.refresh_from_db()
    assert user.keybase_username == 'test'
    assert user.is_keybase_verified is True
