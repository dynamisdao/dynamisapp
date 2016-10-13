import json

from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.policy.models import POLICY_STATUS_ON_P2P_REVIEW, POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, \
    POLICY_STATUS_ON_COMPLETENESS_CHECK, PolicyApplication, ReviewTask
from dynamis.settings import DEBUG


def test_peer_review_submission_api_view_DEPR(user, api_client, factories, gpg_key,
                                              gpg):
    user.keybase_username = "test"
    user.save()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW)
    application_item = factories.IdentityApplicationItemFactory(policy_application=policy)

    submit_review_url = reverse(
        'v1:application-item-submit-peer-review', kwargs={'pk': application_item.pk},
    )

    peer_review_data = {
        'field-a': 'This is field A',
        'field-b': 'This is field B',
        'result': '4',
    }

    data = {
        'signed_message': gpg.sign(json.dumps(peer_review_data, sort_keys=True)).data,
    }

    assert not user.peer_reviews.exists()

    response = api_client.post(submit_review_url, data)
    assert response.status_code == status.HTTP_200_OK, response.data

    assert user.peer_reviews.exists()


def test_review_task_verify_api_view(user, api_client, factories, gpg_key,
                                     gpg):
    user.keybase_username = "test"
    user.save()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW)
    review_task = factories.IdentityApplicationItemFactory(policy_application=policy)

    submit_review_url = reverse(
        'v1:review-tasks-verify', kwargs={'pk': review_task.pk},
    )

    peer_review_data = {
        'field-a': 'This is field A',
        'field-b': 'This is field B',
        'result': '5',
    }

    data = {
        'signed_message': gpg.sign(json.dumps(peer_review_data, sort_keys=True)).data,
    }

    assert not user.peer_reviews.exists()

    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW
    assert review_task.is_finished is False

    response = api_client.post(submit_review_url, data)
    assert response.status_code == status.HTTP_200_OK, response.data

    policy = PolicyApplication.objects.get(pk=policy.pk)
    review_task = ReviewTask.objects.get(pk=review_task.pk)
    if DEBUG:
        assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW
    else:
        assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK

    assert review_task.is_finished is True

    assert user.peer_reviews.exists()


def test_review_task_verify_api_view_not_finished_tasks_exists(user, api_client, factories, gpg_key,
                                                               gpg):
    user.keybase_username = "test"
    user.save()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW)
    review_task = factories.IdentityApplicationItemFactory(policy_application=policy)
    review_task_second = factories.IdentityApplicationItemFactory(policy_application=policy)

    submit_review_url = reverse(
        'v1:review-tasks-verify', kwargs={'pk': review_task.pk},
    )

    peer_review_data = {
        'field-a': 'This is field A',
        'field-b': 'This is field B',
        'result': '5',
    }

    data = {
        'signed_message': gpg.sign(json.dumps(peer_review_data, sort_keys=True)).data,
    }

    assert not user.peer_reviews.exists()

    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW
    assert review_task.is_finished is False

    response = api_client.post(submit_review_url, data)

    assert response.status_code == status.HTTP_200_OK, response.data

    policy = PolicyApplication.objects.get(pk=policy.pk)
    review_task = ReviewTask.objects.get(pk=review_task.pk)
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW

    assert review_task.is_finished is True
    assert review_task_second.is_finished is False

    assert user.peer_reviews.exists()
