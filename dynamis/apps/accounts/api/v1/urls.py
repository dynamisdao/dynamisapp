from __future__ import absolute_import

from django.conf.urls import url

from .views import (
    AccountCreationAPIView,
    ManualKeybaseVerificationView,
    AccountSettingsViewSet)

action_get_put = {'get': 'retrieve', 'put': 'update'}

urlpatterns = [
    # TODO - deprecated
    url(
        r'^account-create/$',
        AccountCreationAPIView.as_view(),
        name="account-create",
    ),
    url(
        r'^verify-keybase/$',
        ManualKeybaseVerificationView.as_view(),
        name="verify-keybase",
    ),
    url(r'^(?P<pk>\w+)/settings/$', AccountSettingsViewSet.as_view(action_get_put),
        name='account-settings-detail'),
]
