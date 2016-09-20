import gnupg

import pytest

from django_webtest import (
    WebTest as BaseWebTest,
    DjangoTestApp as BaseDjangoTestApp,
)


@pytest.fixture()  # NOQA
def factories(transactional_db):
    import factory

    from factories.accounts import (  # NOQA
        UserFactory, AccountConfigFactory
    )
    from factories.policy import (  # NOQA
        PolicyApplicationFactory,
        IdentityApplicationItemFactory,
        EmploymentClaimApplicationItemFactory,
        IdentityPeerReviewFactory,
        EmploymentClaimPeerReviewFactory,
        RiskAssessmentTaskFactory,
    )
    from factories.payments import (
        SmartDepositFactory,
        PremiumPaymentFactory,
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.DjangoModelFactory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models_no_db():
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(models_no_db, transactional_db):
    return models_no_db


class DjangoTestApp(BaseDjangoTestApp):
    def _update_environ(self, environ, user):
        user = user or self.user
        return super(DjangoTestApp, self)._update_environ(environ, user)

    @property
    def user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_id = self.session.get('_auth_user_id')
        if user_id:
            return User.objects.get(pk=user_id)
        else:
            return None


class WebTest(BaseWebTest):
    app_class = DjangoTestApp

    def authenticate(self, user):
        self.app.get('/', user=user)

    def unauthenticate(self):
        self.app.get('/', user=None)


@pytest.fixture()  # NOQA
def webtest_client(transactional_db):
    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app


@pytest.fixture()
def user_webtest_client(webtest_client, user):
    web_test = WebTest(methodName='__call__')
    web_test()
    web_test.authenticate(user)
    return web_test.app


@pytest.fixture()  # NOQA
def User(django_user_model):
    """
    A slightly more intuitively named
    `pytest_django.fixtures.django_user_model`
    """
    return django_user_model


@pytest.fixture()
def admin_user(factories, User):
    try:
        return User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        return factories.UserFactory(
            email='admin@example.com',
            is_superuser=True,
            password='password',
        )


@pytest.fixture()
def user(factories, User):
    try:
        return User.objects.get(email='test@example.com')
    except User.DoesNotExist:
        return factories.UserFactory(
            email='test@example.com',
            password='password',
        )


@pytest.fixture()
def user_client(user, client):
    assert client.login(username=user.email, password='password')
    client.user = user
    return client


@pytest.fixture()
def admin_client(admin_user, client):
    assert client.login(username=admin_user.email, password='password')
    client.user = admin_user
    return client


@pytest.fixture()
def api_client(user, db):
    """
    A rest_framework api test client not auth'd.
    """
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    return client


#
#  Identity Verification Stuff
#
@pytest.fixture
def gpg(tmpdir):
    """
    Provides a GPG Keyring that can be used for tests.
    """
    gpg_home = str(tmpdir.mkdir('gpg-home'))
    gpg = gnupg.GPG(gnupghome=gpg_home)
    return gpg


@pytest.fixture
def generate_gpg_key_raw(gpg):
    """
    Function which generates a new key for the gpg keyring
    """
    def _generate_gpg_key_raw():
        seed = gpg.gen_key_input(key_type="RSA", key_length=1024)
        key = gpg.gen_key(seed)
        return key
    return _generate_gpg_key_raw


@pytest.fixture
def gpg_key_raw(generate_gpg_key_raw):
    """
    A gpg key on the gpg keyring
    """
    return generate_gpg_key_raw()


@pytest.fixture
def dummy_public_key_provider(monkeypatch, settings):
    """
    For mocking out the public key provider
    """
    settings.PUBLIC_KEY_PROVIDER_PATH = 'dynamis.utils.testing.DummyPublicKeyProvider'


@pytest.fixture
def generate_gpg_key(dummy_public_key_provider, gpg, monkeypatch,
                     generate_gpg_key_raw):
    """
    Function that generates a GPG key that can be used with the public key
    provider.
    """
    from dynamis.utils import testing

    def _generate_gpg_key(username):
        gpg_key = generate_gpg_key_raw()
        public_key_pem = gpg.export_keys([gpg_key.fingerprint])
        monkeypatch.setitem(testing.KEY_DB, (username,), public_key_pem)
        monkeypatch.setitem(testing.PROOF_DB, (username,), [])
        return gpg_key
    return _generate_gpg_key


@pytest.fixture
def gpg_key(generate_gpg_key):
    """
    Generates a GPG key and includes it in the dummy public key provider's
    database.
    """
    return generate_gpg_key('test')
