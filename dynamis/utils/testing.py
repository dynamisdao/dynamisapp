from dynamis.apps.identity.providers import BasePublicKeyProvider


KEY_DB = {}
PROOF_DB = {}


class DummyPublicKeyProvider(BasePublicKeyProvider):
    name = 'dummy'

    def get_public_key(self, *args):
        return KEY_DB[args]

    def get_proofs(self, *args):
        return PROOF_DB[args]
