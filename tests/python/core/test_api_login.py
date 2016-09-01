from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from rest_framework import status


def test_login(api_client, factories):
    email = 'test@email.com'
    password = 'test_password'
    login_url = reverse('v1:api-login')
    user = factories.UserFactory(email=email, password=password)
    Session.objects.all().count() == 0

    response = api_client.post(login_url, data={'email': email, 'password': password})

    assert response.status_code == status.HTTP_200_OK
    Session.objects.all().count() == 1


def test_login_wrong_password(api_client, factories):
    email = 'test@email.com'
    password = 'test_password'
    login_url = reverse('v1:api-login')
    user = factories.UserFactory(email=email, password=password)
    Session.objects.all().count() == 0

    response = api_client.post(login_url, data={'email': email, 'password': 'wrong_pass'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    Session.objects.all().count() == 0


def test_logout(api_client, factories):
    email = 'test@email.com'
    password = 'test_password'
    logout_url = reverse('v1:api-logout')
    user = factories.UserFactory(email=email, password=password)
    Session.objects.all().count() == 1

    response = api_client.post(logout_url)

    assert response.status_code == status.HTTP_200_OK
    Session.objects.all().count() == 0
