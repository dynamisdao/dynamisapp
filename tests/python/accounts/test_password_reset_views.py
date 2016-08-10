from django.core import mail
from django.core.urlresolvers import reverse

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def test_initiating_password_reset_with_unknown_email(webtest_client):
    reset_url = reverse('password-reset')
    page = webtest_client.get(reset_url)

    assert len(mail.outbox) == 0

    page.form['email'].value = 'not-a-real-user@example.com'

    response = page.form.submit()
    assert response.status_code == 302

    # see that no email was sent.
    assert len(mail.outbox) == 0


def test_initiating_password_reset(webtest_client, user):
    # Test password reset
    reset_url = reverse('password-reset')
    page = webtest_client.get(reset_url)

    assert len(mail.outbox) == 0

    page.form['email'].value = user.email

    response = page.form.submit()
    assert response.status_code == 302

    # see that no email was sent.
    assert len(mail.outbox) == 1

    message = mail.outbox[0]
    assert message.to[0] == user.email


def test_resetting_password(webtest_client, user):
    # Test changing password from password reset link
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_url = reverse(
        'password-reset-confirm-and-login',
        kwargs={'uidb64': uid, 'token': token},
    )

    # sanity
    assert webtest_client.user is None
    assert not user.check_password('new-password')

    page = webtest_client.get(reset_url)
    page.form['new_password1'].value = 'new-password'
    page.form['new_password2'].value = 'new-password'

    response = page.form.submit()

    assert response.status_code == 302
    assert webtest_client.user == user

    user.refresh_from_db()
    assert user.check_password('new-password')
