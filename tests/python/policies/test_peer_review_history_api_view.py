from django.core.urlresolvers import reverse

from rest_framework import status


def test_peer_review_history_view(factories, api_client, user):
    peer_review_history_url = reverse('v1:peer-review-history-list')

    factories.IdentityPeerReviewFactory.create_batch(5, user=user)

    response = api_client.get(peer_review_history_url)

    assert response.status_code == status.HTTP_200_OK, response.data

    data = response.data

    assert len(data['results']) == 5
