from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from dynamis.apps.accounts.api.v1.views import AccountViewSet

urlpatterns = [
    url(r'^accounts/', include('dynamis.apps.accounts.api.v1.urls')),
    url(r'^application/', include('dynamis.apps.policy.api.v1.urls')),
]

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='accounts')
urlpatterns += router.urls
