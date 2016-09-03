from django.conf.urls import url

from .views import (
    UserIndexView,
    UserUpdateView,
    PolicyIndexViewMixin)


urlpatterns = [
    url(r'^users/$', UserIndexView.as_view(), name='user-index'),
    url(r'^policies/$', PolicyIndexViewMixin.as_view(), name='policy-index'),
    url(r'^users/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user-detail'),
]
