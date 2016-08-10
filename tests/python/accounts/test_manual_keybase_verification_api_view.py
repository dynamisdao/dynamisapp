from django.core import signing
from django.core.urlresolvers import reverse


def test_manual_keybase_verification(api_client, user, gpg_key, gpg, factories):
    keybase_verify_url = reverse('v1:verify-keybase')

    token = signing.dumps(user.pk)

    assert user.keybase_username == ''

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(token).data,
    }

    response = api_client.put(keybase_verify_url, data=data)
    assert response.status_code == 200, response.data

    user.refresh_from_db()
    assert user.keybase_username == 'test'
