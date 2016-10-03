from authtools.views import (
    PasswordChangeView,
)
from constance import config
from django.contrib import messages
from django.core import signing
from django.core.urlresolvers import (
    reverse,
)
from django.db.transaction import atomic
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic import (
    TemplateView,
    RedirectView,
)
from django.views.generic.list import ListView
from django_tables2 import SingleTableMixin

from dynamis.apps.accounts.forms import FillEthOperationForm
from dynamis.apps.accounts.tables import RiskAssessmentTaskTable
from dynamis.apps.payments.models import FillEthOperation, TokenAccount, EthAccount
from dynamis.utils.mixins import LoginRequired
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


class WalletView(LoginRequired, ListView, FormView):
    form_class = FillEthOperationForm
    success_url = '/accounts/wallet/'
    object_list = FillEthOperation.objects.all()
    template_name = "accounts/wallet.html"

    def get(self, request, *args, **kwargs):
        EthAccount.objects.get_or_create(user=request.user)
        return super(WalletView, self).get(request, *args, **kwargs)

    @atomic
    def form_valid(self, form):
        eth_account = EthAccount.objects.filter(user=self.request.user).first()
        eth_account.eth_balance -= float(form.data['amount']) * config.EHT_TOKEN_EXCHANGE_RATE
        eth_account.save()
        token_account, _ = TokenAccount.objects.get_or_create(user=self.request.user)
        token_account.immature_tokens_balance += float(form.data['amount'])
        token_account.save()
        form.save()
        return super(WalletView, self).form_valid(form)

    def get_queryset(self):
        return FillEthOperation.objects.filter(eth_account__in=self.request.user.eth_accounts.filter(is_active=True))


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


