from django.conf.urls import url

from dynamis.apps.policy.views import SmartDepositView, SmartDepositStubView
from .views import (
    PolicyCreateView,
    PolicyEditView,
    PeerReviewItemsView,
)

urlpatterns = [
    url(
        r'^new/$', PolicyCreateView.as_view(),
        name="policy-create",
    ),
    url(
        r'^(?P<pk>[0-9]+)/$', PolicyEditView.as_view(),
        name="policy-edit",
    ),
    url(
        r'^peer-review-items/$', PeerReviewItemsView.as_view(),  # todo
        name="peer-review-items",
    ),
    url(r'^(?P<pk>[0-9]+)/smart-deposit/$', SmartDepositView.as_view(), name='smart-deposit-real'),
    url(r'^(?P<pk>[0-9]+)/smart-deposit-fake/$', SmartDepositStubView.as_view(), name='smart-deposit-stub'),
]
