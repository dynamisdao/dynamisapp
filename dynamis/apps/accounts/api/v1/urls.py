from __future__ import absolute_import

from django.conf.urls import url

from .views import (
    AccountCreationAPIView,
    ManualKeybaseVerificationView,
    AccountConfigViewSet)

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
    url(r'^(?P<user__keybase_username>\w+)/config/$', AccountConfigViewSet.as_view(action_get_put),
        name='account-config-detail'),
]
