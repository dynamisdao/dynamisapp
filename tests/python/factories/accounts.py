import factory

from dynamis.apps.accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence('test-{0}@example.com'.format)

    password = factory.PostGenerationMethodCall('set_password', 'secret')

    class Meta:
        model = User
