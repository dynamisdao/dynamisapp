from django.conf.urls import url

from .views import (
    UserIndexView,
    UserUpdateView,
)


urlpatterns = [
    url(r'^users/$', UserIndexView.as_view(), name='user-index'),
    url(r'^users/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user-detail'),
]
