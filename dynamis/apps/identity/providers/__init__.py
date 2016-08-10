from django.conf import settings
from django.utils.module_loading import import_string


class BasePublicKeyProvider(object):
    """
    Base class for public key providers.
    """
    @property
    def name(self):
        raise NotImplementedError('Public key providers must specify a unique name')

    def get_public_key(self, *args, **kwargs):
        raise NotImplementedError('Public key providers must implement a `get_public_key` method')


def get_provider_class(provider_path=None):
    return import_string(provider_path or settings.PUBLIC_KEY_PROVIDER_PATH)


def get_provider(provider_path=None):
    provider_class = get_provider_class(provider_path)
    return provider_class()
