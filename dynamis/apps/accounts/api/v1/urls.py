from __future__ import absolute_import

from django.conf.urls import url

from .views import (
    AccountCreationAPIView,
    DEPR_ManualKeybaseVerificationView,
    AccountSettingsViewSet, ManualKeybaseVerificationViewSet)

action_get_put = {'get': 'retrieve', 'put': 'update'}

urlpatterns = [
    # TODO - deprecated
    url(
        r'^account-create/$',
        AccountCreationAPIView.as_view(),
        name="account-create",
    ),
    # TODO - deprecated
    url(
        r'^verify-keybase/$',
        DEPR_ManualKeybaseVerificationView.as_view(),
        name="verify-keybase",
    ),
    url(
        r'^(?P<pk>\d+)/keybase/$',
        ManualKeybaseVerificationViewSet.as_view({'put': 'update'}),
        name="verify-keybase-detail",
    ),
    url(r'^(?P<pk>\d+)/settings/$', AccountSettingsViewSet.as_view(action_get_put),
        name='account-settings-detail'),
]
