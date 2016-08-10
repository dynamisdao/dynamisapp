from django.conf.urls import url
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
]
