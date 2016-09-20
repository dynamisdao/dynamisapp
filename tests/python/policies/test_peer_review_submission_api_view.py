import json

from django.core.urlresolvers import reverse

from rest_framework import status


def test_peer_review_submission_api_view(user, api_client, factories, gpg_key,
                                         gpg):
    user.keybase_username = "test"
    user.save()
    application_item = factories.IdentityApplicationItemFactory()

    submit_review_url = reverse(
        'v1:application-item-submit-peer-review', kwargs={'pk': application_item.pk},
    )

    peer_review_data = {
        'field-a': 'This is field A',
        'field-b': 'This is field B',
        'result': '1',
    }

    data = {
        'signed_message': gpg.sign(json.dumps(peer_review_data, sort_keys=True)).data,
    }

    assert not user.peer_reviews.exists()

    response = api_client.post(submit_review_url, data)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

    assert user.peer_reviews.exists()


def test_review_task_verify_api_view(user, api_client, factories, gpg_key,
                                         gpg):
    user.keybase_username = "test"
    user.save()
    application_item = factories.IdentityApplicationItemFactory()

    submit_review_url = reverse(
        'v1:review-tasks-verify', kwargs={'pk': application_item.pk},
    )

    peer_review_data = {
        'field-a': 'This is field A',
        'field-b': 'This is field B',
        'result': '1',
    }

    data = {
        'signed_message': gpg.sign(json.dumps(peer_review_data, sort_keys=True)).data,
    }

    assert not user.peer_reviews.exists()

    response = api_client.post(submit_review_url, data)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

    assert user.peer_reviews.exists()
