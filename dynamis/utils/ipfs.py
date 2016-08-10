import ipfsApi

from django.conf import settings


def get_ipfs_client(host=None, port=None, **kwargs):
    if not host and not settings.IPFS_HOST:
        raise ValueError("Must either specify a host or set the `IPFS_HOST` setting")
    elif not host:
        host = settings.IPFS_HOST

    if port is None:
        port = settings.IPFS_PORT

    if not settings.IPFS_SSL_VERIFY:
        kwargs.setdefault('verify', False)

    if settings.IPFS_AUTH_USERNAME:
        http_credentials = (settings.IPFS_AUTH_USERNAME, settings.IPFS_AUTH_PASSWORD)
        kwargs.setdefault('auth', http_credentials)

    client = ipfsApi.Client(host, port, **kwargs)
    return client
