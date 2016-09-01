from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from dynamis.apps.accounts.api.v1.views import AccountViewSet
from dynamis.core.api.v1.views import LoginView, LogoutView

urlpatterns = [
    url(r'^accounts/', include('dynamis.apps.accounts.api.v1.urls')),
    url(r'^application/', include('dynamis.apps.policy.api.v1.urls')),
    url(r'^login/', LoginView.as_view(), name='api-login'),
    url(r'^logout/', LogoutView.as_view(), name='api-logout'),
]

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='accounts')
urlpatterns += router.urls
