from django.core.urlresolvers import reverse

from rest_framework import status

from dynamis.apps.policy.api.v1.serializers import ApplicationItemSerializer


def test_review_tasks_get_api_view(user, api_client, factories, gpg_key,
                                   gpg):
    application_item = factories.IdentityApplicationItemFactory()

    url = reverse(
        'v1:review-tasks-detail', kwargs={'pk': application_item.pk},
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == ApplicationItemSerializer(application_item).data


def test_review_tasks_list_api_view(user, api_client, factories, gpg_key,
                                    gpg):
    application_item = factories.IdentityApplicationItemFactory()
    application_item_2 = factories.IdentityApplicationItemFactory()

    app_item_list = (application_item, application_item_2)

    url = reverse('v1:review-tasks-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == ApplicationItemSerializer(app_item_list, many=True).data


def test_review_tasks_list_api_view_hide_finished(user, api_client, factories, gpg_key,
                                                  gpg):
    application_item = factories.IdentityApplicationItemFactory()
    application_item_2 = factories.IdentityApplicationItemFactory()
    application_item_3 = factories.IdentityApplicationItemFactory(is_finished=True)

    app_item_list = (application_item, application_item_2)

    url = reverse('v1:review-tasks-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == ApplicationItemSerializer(app_item_list, many=True).data
