from django.core.urlresolvers import reverse


def test_logging_out(user_webtest_client):
    logout_url = reverse('logout')

    # sanity check
    assert user_webtest_client.user is not None

    page = user_webtest_client.get(logout_url)

    assert page.status_code == 302
    assert user_webtest_client.user is None


def test_logging_out_not_logged_in(webtest_client):
    logout_url = reverse('logout')

    # sanity check
    assert webtest_client.user is None

    page = webtest_client.get(logout_url)

    assert page.status_code == 302
    assert webtest_client.user is None
