from django.core import mail
from django.core.urlresolvers import reverse

from rest_framework import status


def test_user_creation_api_view(User, api_client):
    account_create_url = reverse('v1:account-create')
    test_email = 'test-1@example.com'

    #print("Account creation URL is: {}".format(account_create_url))

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
    assert response.status_code == status.HTTP_200_OK, response.data

    # Make sure verification email was sent.
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to[0] == test_email

    assert User.objects.filter(email=test_email).exists()

    # see that we were logged in.
    assert '_auth_user_id' in api_client.session.keys()
