from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.payments.models import SmartDeposit
from dynamis.apps.policy.business_logic import how_long_stay_answer_coasts, unemployment_period_answer_coasts
from dynamis.apps.policy.models import PolicyApplication, EmploymentHistoryJob, POLICY_STATUS_SUBMITTED, \
    POLICY_STATUS_INIT


def test_create_policy(user, api_client, policy_data, job_data, questions_data):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)
    policy_data['questions'].update(questions_data)

    assert PolicyApplication.objects.all().count() == 0
    url = reverse('v1:policy-list-new')
    response = api_client.post(url, data={'data': policy_data})
    assert response.status_code == status.HTTP_200_OK
    assert PolicyApplication.objects.all().count() == 1
    assert EmploymentHistoryJob.objects.all().count() == 1
    policy = PolicyApplication.objects.get()
    assert policy.how_long_stay_answer == policy_data['questions']['howLongStay']
    assert policy.unemployment_period_answer == policy_data['questions']['unemploymentPeriod']
    coast_one = how_long_stay_answer_coasts[policy_data['questions']['howLongStay']]
    coast_two = unemployment_period_answer_coasts[policy_data['questions']['unemploymentPeriod']]
    assert SmartDeposit.objects.get().coast == coast_one + coast_two


def test_create_policy_no_answers_in_data(user, api_client, policy_data, job_data):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    assert PolicyApplication.objects.all().count() == 0
    url = reverse('v1:policy-list-new')
    response = api_client.post(url, data={'data': policy_data})
    assert response.status_code == status.HTTP_200_OK
    policy = PolicyApplication.objects.get()
    assert policy.how_long_stay_answer == 0
    assert policy.unemployment_period_answer == 0


def test_create_policy_no_data(user, api_client):
    assert PolicyApplication.objects.all().count() == 0
    url = reverse('v1:policy-list-new')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert PolicyApplication.objects.all().count() == 1
    assert EmploymentHistoryJob.objects.all().count() == 0


def test_update_policy(user, api_client, policy_data, job_data, factories, questions_data):
    policy = factories.PolicyApplicationFactory()
    policy_data['questions'].update(questions_data)

    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    assert policy.how_long_stay_answer is None
    assert policy.unemployment_period_answer is None

    url = reverse('v1:policy-detail-new', args=[policy.pk])
    response = api_client.put(url, data={'data': policy_data})
    assert response.status_code == status.HTTP_200_OK
    assert PolicyApplication.objects.all().count() == 1
    assert EmploymentHistoryJob.objects.all().count() == 1
    policy = PolicyApplication.objects.get()
    assert policy.how_long_stay_answer == policy_data['questions']['howLongStay']
    assert policy.unemployment_period_answer == policy_data['questions']['unemploymentPeriod']
    coast_one = how_long_stay_answer_coasts[policy_data['questions']['howLongStay']]
    coast_two = unemployment_period_answer_coasts[policy_data['questions']['unemploymentPeriod']]
    assert SmartDeposit.objects.get().coast == coast_one + coast_two


def test_update_policy_check_cancel_submission(user, api_client, policy_data, job_data, factories, questions_data):
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED)

    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)
    policy_data['questions'].update(questions_data)

    url = reverse('v1:policy-detail-new', args=[policy.pk])
    response = api_client.put(url, data={'data': policy_data})
    assert response.status_code == status.HTTP_200_OK
    assert PolicyApplication.objects.all().count() == 1
    assert EmploymentHistoryJob.objects.all().count() == 1
    assert PolicyApplication.objects.all().first().state == POLICY_STATUS_INIT
