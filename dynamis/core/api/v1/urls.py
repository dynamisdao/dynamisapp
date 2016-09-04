from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from dynamis.apps.accounts.api.v1.views import AccountViewSet
from dynamis.apps.policy.api.v1.views import PolicyApplicationViewSet
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
        name="policy-detail",
    ),
    url(
        r'^policies/(?P<pk>\d+)/signature$',
        PolicyApplicationViewSet.as_view({'post': 'submit'}),
        name="policy-signature",
    ),
    url(
        r'^policies/(?P<pk>\d+)/file',
        PolicyApplicationViewSet.as_view({'post': 'upload_file'}),
        name="policy-file",
    ),
    url(
        r'^policies/$',
        PolicyApplicationViewSet.as_view({'post': 'create'}),
        name="policy-list",
    ),
    url(
        r'admin/policies/$',
        PolicyApplicationViewSet.as_view({'get': 'list'}),
        name="policy-admin-list",
    ),
]

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='accounts')
urlpatterns += router.urls
