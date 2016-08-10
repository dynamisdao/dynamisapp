from django.core.urlresolvers import reverse


def test_logging_in(webtest_client, factories):
    login_url = reverse('login')

    user = factories.UserFactory()

    page = webtest_client.get(login_url)

    page.form['username'] = user.email
    page.form['password'] = 'secret'

    # sanity check
    assert webtest_client.user is None

    response = page.form.submit()

    assert response.status_code == 302
    assert webtest_client.user == user


def test_logging_bad_password(webtest_client, factories):
    login_url = reverse('login')

    user = factories.UserFactory()

    page = webtest_client.get(login_url)

    page.form['username'] = user.email
    page.form['password'] = 'bad_password'

    # sanity check
    assert webtest_client.user is None

    response = page.form.submit()

    assert response.status_code == 200
    assert webtest_client.user is None
