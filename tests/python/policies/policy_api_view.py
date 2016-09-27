from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.policy.api.v1.serializers import ApplicationItemSerializer
from dynamis.apps.policy.models import PolicyApplication


def test_create_policy_no_data(user, api_client):

    assert PolicyApplication.objects.all().count() == 0
    url = reverse('v1:policy-list-new')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert PolicyApplication.objects.all().count() == 1
