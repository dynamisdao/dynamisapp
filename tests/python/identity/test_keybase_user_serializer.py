from dynamis.apps.identity.providers.keybase import KeybaseUserSerializer


fixture = {
    "status": {
        "code": 0,
        "name": "OK",
    },
    "them": {
        "basics": {
            "username": "pipermerriam",
        }
    }
}


# TODO: need more comprehensive tests.  no error cases are covered here.


def test_keybase_user_serializer():
    serializer = KeybaseUserSerializer(fixture['them'])
    data = serializer.data
    assert data['username'] == 'pipermerriam'


def test_keybase_user_serializer_validation():
    serializer = KeybaseUserSerializer(data=fixture)
    serializer.is_valid(raise_exception=True)

    data = serializer.save()
    assert data == fixture['them']
