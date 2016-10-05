from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.policy.models import PolicyApplication, EmploymentHistoryJob


def test_create_policy(user, api_client, policy_data, job_data):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    assert PolicyApplication.objects.all().count() == 0
    url = reverse('v1:policy-list-new')
    response = api_client.post(url, data={'data': policy_data})
    assert response.status_code == status.HTTP_201_CREATED
    assert PolicyApplication.objects.all().count() == 1
    assert EmploymentHistoryJob.objects.all().count() == 1


def test_create_policy_no_data(user, api_client):
    assert PolicyApplication.objects.all().count() == 0
    url = reverse('v1:policy-list-new')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert PolicyApplication.objects.all().count() == 1
    assert EmploymentHistoryJob.objects.all().count() == 0


def test_update_policy(user, api_client, policy_data, job_data, factories):
    policy = factories.PolicyApplicationFactory()

    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    url = reverse('v1:policy-detail-new', args=[policy.pk])
    response = api_client.put(url, data={'data': policy_data})
    assert response.status_code == status.HTTP_200_OK
    assert PolicyApplication.objects.all().count() == 1
    assert EmploymentHistoryJob.objects.all().count() == 1
