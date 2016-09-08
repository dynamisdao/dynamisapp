from __future__ import absolute_import

from rest_framework import routers

from .views import (
    PolicyApplicationViewSet,
    ApplicationItemReviewQueueViewSet,
    PeerReviewHistoryViewSet,
    RiskAssessmentTaskViewSet)


router = routers.SimpleRouter()

# TODO DEPRECATED
router.register(r'policies', PolicyApplicationViewSet, 'policy')

router.register(r'application-items', ApplicationItemReviewQueueViewSet, 'application-item')
router.register(r'peer-review-history', PeerReviewHistoryViewSet, 'peer-review-history')
router.register(r'assessment_tasks', RiskAssessmentTaskViewSet, 'assessment_tasks')

urlpatterns = router.urls
