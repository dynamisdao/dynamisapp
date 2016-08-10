from django.core import signing

from dynamis.apps.accounts.api.v1.serializers import VerifyKeybaseSerializer


def test_manual_keybase_verification(user, gpg_key, gpg, factories):
    assert user.keybase_username == ''

    token = signing.dumps(user.pk)

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(token).data,
    }

    serializer = VerifyKeybaseSerializer(user, data=data)

    assert serializer.is_valid(), serializer.errors

    user = serializer.save()

    assert user.keybase_username == 'test'
