from django.core.urlresolvers import (
    reverse,
)
from django.core import signing
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
