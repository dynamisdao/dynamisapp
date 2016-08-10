from django.conf.urls import url, include


urlpatterns = [
    url(r'^accounts/', include('dynamis.apps.accounts.api.v1.urls')),
    url(r'^application/', include('dynamis.apps.policy.api.v1.urls')),
]
