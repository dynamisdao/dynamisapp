from django.core.urlresolvers import (
    reverse,
)
from django.core import signing
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import (
    TemplateView,
    RedirectView,
)
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect

from authtools.views import (
    PasswordChangeView,
)
from dynamis.apps.accounts.tables import RiskAssessmentTaskTable
from django.views.generic.list import ListView
from django_tables2 import SingleTableMixin

from dynamis.apps.accounts.forms import SmartDepositStubForm
from dynamis.apps.accounts.tables import SmartDepositTable
from dynamis.apps.payments.models import SmartDeposit
from dynamis.apps.policy.models import POLICY_STATUS_INIT, POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, \
    POLICY_STATUS_ON_P2P_REVIEW, POLICY_STATUS_SUBMITTED
from dynamis.utils.mixins import LoginRequired
from dynamis.apps.accounts.tables import RiskAssessmentTaskTable

from .models import User


class KeybaseVerificationView(LoginRequired, TemplateView):
    template_name = "accounts/verify_keybase.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated() and self.request.user.keybase_username:
            return redirect(reverse('user-profile'))
        return super(KeybaseVerificationView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(KeybaseVerificationView, self).get_context_data(**kwargs)
        context['token'] = signing.dumps(self.request.user.pk)
        return context


class UserDashboardView(LoginRequired, TemplateView):
    template_name = "accounts/user_dashboard.html"


class AssessorDashboardView(LoginRequired, SingleTableMixin, ListView):
    template_name = "accounts/assessor_dashboard.html"
    table_class = RiskAssessmentTaskTable

    def get_queryset(self):
        return self.request.user.risk_assessment_tasks.all()


class RiskAssessmentView(LoginRequired, TemplateView):
    template_name = "accounts/risk_assessment.html"

    def get_object(self):
        return self.request.user.risk_assessment_tasks.get(pk=self.kwargs['pk'])


class MyPolicyView(LoginRequired, TemplateView):
    template_name = "accounts/my_policy.html"


class WalletView(TemplateView):
    template_name = "accounts/wallet.html"


class NotifyingPasswordChangeView(PasswordChangeView):
    """
    Adds a message using the django messages framework to notify the user of a
    successful password change.
    """

    def form_valid(self, *args, **kwargs):
        messages.success(self.request, "Your password has been updated")
        return super(NotifyingPasswordChangeView, self).form_valid(*args, **kwargs)


class VerifyEmailView(RedirectView):
    """
    Given a valid activation key, activate the user's
    alternate email. Pulled from django-registration.
    """

    def get_redirect_url(self, *args, **kwargs):
        if self.activate():
            messages.success(self.request, "Your email address has been verified")
        else:
            messages.error(self.request, "Unable to verify your email")
        return reverse('user-profile')

    def activate(self, *args, **kwargs):
        email = self.validate_key(self.kwargs.get('activation_key'))
        if email is not None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return False

            user.verified_at = timezone.now()
            user.save()
            return True
        return False

    def validate_key(self, activation_key):
        """
        Verify that the activation key is valid and within the
        permitted activation time window, returning the email if
        valid or ``None`` if not.
        """
        try:
            email = signing.loads(
                activation_key,
                salt="registration",
            )
            return email
        # SignatureExpired is a subclass of BadSignature, so this will
        # catch either one.
        except signing.BadSignature:
            return None


class SmartDepositStubView(LoginRequired, SingleTableMixin, FormView, ListView):
    template_name = "accounts/smart-deposit-stub.html"
    form_class = SmartDepositStubForm
    table_class = SmartDepositTable
    success_url = '/'

    def get_queryset(self):
        return SmartDeposit.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.save()
        policy = self.request.user.policies.all()[0]
        if policy.state == POLICY_STATUS_INIT:
            policy.submit()
        elif policy.state == POLICY_STATUS_SUBMITTED:
            policy.submit_to_p2p_review()
            policy.save()
        return super(SmartDepositStubView, self).form_valid(form)
