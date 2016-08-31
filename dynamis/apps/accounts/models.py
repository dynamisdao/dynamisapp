from __future__ import unicode_literals

import ogmios

from authtools.models import AbstractEmailUser
from django.conf import settings
from django.core import signing
from django.db import models
from django.contrib.sites.models import Site


class User(AbstractEmailUser):
    verified_at = models.DateTimeField(null=True, blank=True)
    keybase_username = models.CharField(max_length=16, blank=True)
    is_keybase_verified = models.BooleanField(default=False)

    is_risk_assessor = models.BooleanField(
        default=False,
        help_text="Determines whether this user can participate as a risk assessor",
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff

    def send_verification_email(self, protocol='https'):
        """
        Send the verification email. The activation key is simply the
        username, signed using TimestampSigner.
        """
        activation_key = signing.dumps(
            obj=self.email,
            salt="registration"
        )

        ogmios.send_email('mail/verification.html', {
            'site': Site.objects.get_current(),
            'protocol': protocol,
            'to_email': self.email,
            'from': settings.DEFAULT_FROM_EMAIL,
            'activation_key': activation_key,
        })

    def get_keybase_username(self):
        return self.keybase_username


class AccountConfig(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    rpc_node_host = models.URLField(default='http://localhost:8545')
