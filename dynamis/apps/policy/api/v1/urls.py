from __future__ import absolute_import

from rest_framework import routers

from .views import (
    PolicyApplicationViewSet,
    ApplicationItemReviewQueueViewSet,
    PeerReviewHistoryViewSet,
)


router = routers.SimpleRouter()

# TODO DEPRECATED
router.register(r'policies', PolicyApplicationViewSet, 'policy-depr')

router.register(r'application-items', ApplicationItemReviewQueueViewSet, 'application-item')
router.register(r'peer-review-history', PeerReviewHistoryViewSet, 'peer-review-history')

urlpatterns = router.urls
