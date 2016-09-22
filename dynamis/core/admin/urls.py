from django.conf.urls import url, include

from .views import (
    AdminIndexView,
)


urlpatterns = [
    url(r'^$', AdminIndexView.as_view(), name='site-index'),
    url(r'^accounts/', include('dynamis.apps.accounts._admin.urls')),
]
