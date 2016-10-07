import datetime
from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer
from dynamis.apps.payments.models import SmartDeposit


def test_get_smart_deposit_ok(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=1,
                                            wait_for=datetime.datetime.now() - datetime.timedelta(minutes=5))
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert response.data == SmartDepositShortSerializer(deposit).data


def test_get_smart_deposit_wait_expired(user_webtest_client, api_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    deposit = factories.SmartDepositFactory(policy=policy, state=1,
                                            wait_for=datetime.datetime.now() - datetime.timedelta(minutes=5))
    assert SmartDeposit.objects.get().state == 1
    url = reverse('v1:smart_deposit-detail', args=[policy.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    deposit = SmartDeposit.objects.get()
    assert deposit.state == 0
