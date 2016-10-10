import json

from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.payments.models import SmartDeposit, SMART_DEPOSIT_STATUS_WAITING, SMART_DEPOSIT_STATUS_INIT
from dynamis.apps.policy.models import PolicyApplication, POLICY_STATUS_SUBMITTED, EmploymentHistoryJob
from dynamis.apps.policy.validation import validate_policy_application
from dynamis.utils import testing


def test_policy_submission_with_valid_data_DEPR(gpg_key, gpg, factories, api_client,
                                           user, policy_data, monkeypatch, job_data):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    monkeypatch.setitem(testing.PROOF_DB, ('test',), policy_data['identity']['verification_data']['proofs'])

    # sanity check that we are using valid test data.
    validate_policy_application(policy_data)

    policy_application = factories.PolicyApplicationFactory(
        user=user,
        data=json.dumps(policy_data),
    )
    # sanity check that it isn't already finalized
    assert not policy_application.is_final

    submit_url = reverse('v1:policy-submit', kwargs={'pk': policy_application.pk})

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(policy_application.data).data,
    }

    response = api_client.post(submit_url, data)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

    policy_application = PolicyApplication.objects.get()
    assert policy_application.is_final is True

    assert policy_application.items.count() == 2

    assert policy_application.state == POLICY_STATUS_SUBMITTED


def test_policy_submission_with_valid_data(gpg_key, gpg, factories, api_client,
                                           user, policy_data, monkeypatch, job_data):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    monkeypatch.setitem(testing.PROOF_DB, ('test',), policy_data['identity']['verification_data']['proofs'])

    # sanity check that we are using valid test data.
    validate_policy_application(policy_data)

    policy_application = factories.PolicyApplicationFactory(
        user=user,
        data=json.dumps(policy_data),
    )
    # sanity check that it isn't already finalized
    assert not policy_application.is_final

    submit_url = reverse('v1:policy-signature-new', kwargs={'pk': policy_application.pk})

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(policy_application.data).data,
    }

    response = api_client.post(submit_url, data)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

    policy_application = PolicyApplication.objects.get()
    assert policy_application.is_final is True

    assert policy_application.items.count() == 2

    assert policy_application.state == POLICY_STATUS_SUBMITTED

    smart_deposit = SmartDeposit.objects.get(policy=policy_application)
    assert smart_deposit.state == SMART_DEPOSIT_STATUS_WAITING
