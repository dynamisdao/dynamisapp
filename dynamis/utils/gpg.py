import contextlib

import gnupg


@contextlib.contextmanager
def gpg_keyring(public_key_pem):
    from .filesystem import tempdir

    with tempdir() as gpg_directory:
        gpg = gnupg.GPG(gnupghome=gpg_directory)
        gpg.import_keys(public_key_pem)

        yield gpg
