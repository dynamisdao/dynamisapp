from django.core.urlresolvers import reverse


def test_changing_password(user_webtest_client):
    url = reverse('password-change')

    user = user_webtest_client.user
    user.set_password('my_old_password')
    user.save()

    page = user_webtest_client.get(url)

    page.form['old_password'] = 'my_old_password'
    page.form['new_password1'] = 'my_new_password'
    page.form['new_password2'] = 'my_new_password'

    assert user_webtest_client.user.check_password('my_old_password')
    assert not user_webtest_client.user.check_password('my_new_password')

    response = page.form.submit()

    assert user_webtest_client.user is not None

    user_webtest_client.user.refresh_from_db()

    assert response.status_code == 302

    assert not user_webtest_client.user.check_password('my_old_password')
    assert user_webtest_client.user.check_password('my_new_password')
