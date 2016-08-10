import re

from django.core import mail
from django.core.urlresolvers import reverse

from dynamis.apps.accounts.models import User


def test_verify_email(user_webtest_client):
    test_email = 'test-1@example.com'

    mail.outbox = []

    u = User.objects.create_user(test_email)
    u.send_verification_email()

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to[0] == test_email

    body = mail.outbox[0].body
    match = re.search(r'email\/([-_\w:]+)\/', body)
    assert match is not None, "Pattern not found in {0}".format(body)

    verify_key = match.group(1)

    url = reverse('verify-email', args=[verify_key])

    page = user_webtest_client.get(url)

    assert page.status_code == 302
    assert page.location == reverse('user-profile')

    assert User.objects.filter(pk=u.pk, verified_at__isnull=False).exists()
