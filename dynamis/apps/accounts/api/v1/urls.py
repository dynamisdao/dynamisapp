from __future__ import absolute_import

from django.conf.urls import url

from .views import (
    AccountCreationAPIView,
    ManualKeybaseVerificationView,
    )

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
]
