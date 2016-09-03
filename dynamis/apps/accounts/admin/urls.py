from django.conf.urls import url

from .views import (
    UserIndexView,
    UserUpdateView,
    PolicyIndexView, PolicyInfoView)


urlpatterns = [
    url(r'^users/$', UserIndexView.as_view(), name='user-index'),
    url(r'^users/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user-detail'),
    url(r'^policies/$', PolicyIndexView.as_view(), name='policy-index'),
    url(r'^policies/(?P<pk>\d+)/$', PolicyInfoView.as_view(), name='policy-detail'),
]
