"""dynamis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from dynamis.apps.accounts.views import RootView

admin.autodiscover()

urlpatterns = [
    url(
        r'^$', RootView.as_view(),
        name="site-index",
    ),

    # Apps
    url(r'^accounts/', include('dynamis.apps.accounts.urls')),
    url(r'^policies/', include('dynamis.apps.policy.urls')),

    # API
    url(r'^api/v1/', include('dynamis.core.api.v1.urls', namespace="v1")),

    # Admin
    url(r'^admin/', include('dynamis.core.admin.urls', namespace="admin-namespace")),

]

# Django admin
urlpatterns += [
    url(r'^native-admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
