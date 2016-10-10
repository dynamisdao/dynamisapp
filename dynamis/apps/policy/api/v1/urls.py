from __future__ import absolute_import

from rest_framework import routers

from dynamis.apps.payments.api.v1.views import SmartDepositViewSet
from .views import (
    PolicyApplicationViewSet,
    ReviewTasksViewSet,
    PeerReviewHistoryViewSet,
    RiskAssessmentTaskViewSet)


router = routers.SimpleRouter()

# TODO DEPRECATED
router.register(r'policies', PolicyApplicationViewSet, 'policy')

# TODO DEPRECATED
router.register(r'application-items', ReviewTasksViewSet, 'application-item')

router.register(r'peer-review-history', PeerReviewHistoryViewSet, 'peer-review-history')
router.register(r'assessment_tasks', RiskAssessmentTaskViewSet, 'assessment_tasks')

urlpatterns = router.urls
