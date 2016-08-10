import requests

from rest_framework import serializers

from dynamis.apps.identity.providers import BasePublicKeyProvider


class KeybaseStatusSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField(required=False)

    def validate(self, data):
        if data['code'] != 0:
            raise serializers.ValidationError("{name}: {desc}".format(
                name=data['name'],
                desc=data.get('desc', "Unknown Error"),
            ))
        return data


class KeybaseUserSerializer(serializers.Serializer):
    # Incoming Validation Fields
    status = KeybaseStatusSerializer(write_only=True)
    them = serializers.JSONField(write_only=True)

    # Serialization
    username = serializers.CharField(source="basics.username", read_only=True)
    full_name = serializers.CharField(source="profile.full_name", read_only=True)
    public_key = serializers.CharField(source="public_keys.primary.bundle", read_only=True)
    proofs = serializers.ListField(
        source="proofs_summary.all",
        read_only=True,
        child=serializers.DictField(),
    )

    def create(self, validated_data):
        return validated_data['them']


KEYBASE_LOOKUP_URL = "https://keybase.io/_/api/1.0/user/lookup.json"


class KeybasePublicKeyProvider(BasePublicKeyProvider):
    name = 'keybase'

    def _lookup_user_data(self, username):
        params = {'username': username}
        response = requests.get(KEYBASE_LOOKUP_URL, params=params)
        # TODO: better error handling here
        response.raise_for_status()

        # Perform validation on the keybase response
        serializer = KeybaseUserSerializer(data=response.json())
        serializer.is_valid(raise_exception=True)

        # Convert the keybase response into the format we expect
        user_data = serializer.save()
        return KeybaseUserSerializer(user_data).data

    def get_public_key(self, username):
        user_data = self._lookup_user_data(username)
        if 'public_key' in user_data:
            return user_data['public_key']
        raise serializers.ValidationError("Keybase user does not have a public key")

    def get_proofs(self, username):
        user_data = self._lookup_user_data(username)
        return user_data.get('proofs', [])
