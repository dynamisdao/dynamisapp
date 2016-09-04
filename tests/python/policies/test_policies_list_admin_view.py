from django.core.urlresolvers import reverse
from rest_framework import status

from dynamis.apps.policy.api.v1.serializers import PolicyApplicationSerializer


def test_list_accounts_if_admin(api_client, factories):
    policy_1 = factories.PolicyApplicationFactory()
    policy_2 = factories.PolicyApplicationFactory()
    user_admin = factories.UserFactory(is_staff=True)
    api_client.force_authenticate(user_admin)

    url = reverse('v1:policy-admin-list')
    response = api_client.get(url)

    assert response.data['count'] == 2
    assert response.data['results'][0] == PolicyApplicationSerializer(policy_1).data
    assert response.data['results'][1] == PolicyApplicationSerializer(policy_2).data
    assert response.status_code == status.HTTP_200_OK


def test_deny_list_accounts_if_not_admin(user_webtest_client, api_client, factories):
    policy_1 = factories.PolicyApplicationFactory()
    policy_2 = factories.PolicyApplicationFactory()
    user_admin = factories.UserFactory()
    api_client.force_authenticate(user_admin)

    url = reverse('v1:policy-admin-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
