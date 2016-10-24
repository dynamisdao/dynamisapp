from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from authtools.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmAndLoginView,
)

from .views import (
    KeybaseVerificationView,
    UserDashboardView,
    MyPolicyView,
    AssessorDashboardView,
    RiskAssessmentView,
    VerifyEmailView,
    NotifyingPasswordChangeView,
    WalletView)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(pattern_name='login'), name='logout'),
    url(
        r'^password-reset/$',
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
        ),
        name='password-reset',
    ),
    url(
        r'^password-reset-done/$', PasswordResetDoneView.as_view(),
        name='password-reset-done',
    ),
    url(
        r'^password-reset-done/$', PasswordResetDoneView.as_view(),
        name='password_reset_done',  # authtools uses underscore view names.
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmAndLoginView.as_view(),
        name='password-reset-confirm-and-login',
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmAndLoginView.as_view(),
        name='password_reset_confirm',
    ),
    url(r'^profile/$', UserDashboardView.as_view(), name='user-profile'),
    url(r'^my-policy/$', MyPolicyView.as_view(), name='my-policy'),
    url(r'^wallet/$', WalletView.as_view(), name='wallet'),
    url(
        r'^change-password/$', NotifyingPasswordChangeView.as_view(
            template_name='accounts/change_password.html',
            success_url=reverse_lazy('user-profile'),
        ), name='password-change',
    ),
    url(
        r'^verify-email/(?P<activation_key>[-:\w]+)/$', VerifyEmailView.as_view(),
        name='verify-email'),
    url(r'^verify-keybase/', KeybaseVerificationView.as_view(), name='verify-keybase'),

    url(r'^assessor-dashboard/$', AssessorDashboardView.as_view(), name='assessor-dashboard'),

    url(r'^risk-assessment/(?P<assessment_pk>[0-9]+)/$', RiskAssessmentView.as_view(), name='risk-assessment'),

]
