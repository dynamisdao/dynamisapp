from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from dynamis.apps.accounts.api.v1.views import AccountViewSet
from dynamis.apps.payments.api.v1.views import SmartDepositViewSet, SmartDepositSendView
from dynamis.apps.policy.api.v1.views import PolicyApplicationViewSet, ReviewTasksViewSet
from dynamis.core.api.v1.views import LoginView, LogoutView

action_get_put = {'get': 'retrieve', 'put': 'update'}

urlpatterns = [
    url(r'^accounts/', include('dynamis.apps.accounts.api.v1.urls')),
    url(r'^application/', include('dynamis.apps.policy.api.v1.urls')),
    url(r'^login/', LoginView.as_view(), name='api-login'),
    url(r'^logout/', LogoutView.as_view(), name='api-logout'),
    url(
        r'^policies/(?P<pk>\d+)/$',
        PolicyApplicationViewSet.as_view(action_get_put),
        name="policy-detail-new",
    ),
    url(
        r'^policies/(?P<pk>\d+)/signature$',
        PolicyApplicationViewSet.as_view({'post': 'submit'}),
        name="policy-signature-new",
    ),
    url(
        r'^policies/(?P<pk>\d+)/file$',
        PolicyApplicationViewSet.as_view({'post': 'upload_file'}),
        name="policy-file-new",
    ),
    url(
        r'^policies/(?P<pk>\d+)/smart_deposit$',
        SmartDepositViewSet.as_view({'get': 'retrieve'}),
        name="smart_deposit-detail",
    ),
    url(
        r'^policies/$',
        PolicyApplicationViewSet.as_view({'post': 'create'}),
        name="policy-list-new",
    ),
    url(
        r'admin/policies/$',
        PolicyApplicationViewSet.as_view({'get': 'list'}),
        name="policy-admin-list-new",
    ),
    url(
        r'^policies/(?P<pk>\d+)/smart_deposit/send$',
        SmartDepositSendView.as_view({'post': 'send'}),
        name="send-smart-deposit",
    ),
]

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='accounts')
router.register(r'review-tasks', ReviewTasksViewSet, base_name='review-tasks')
urlpatterns += router.urls
