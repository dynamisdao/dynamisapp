import datetime

from django.contrib.auth import get_user_model
from django.core import signing

from rest_framework import serializers

from dynamis.apps.accounts.models import AccountConfig
from dynamis.apps.identity import get_provider
from dynamis.utils.gpg import gpg_keyring
from dynamis.utils.validation import validate_signature

User = get_user_model()


class AccountCreationSerializer(serializers.Serializer):
    default_error_messages = {
        'password_mismatch': "Passwords do not match",
        'duplicate_email': "A user with this email address already exists",
    }

    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    keybase_username = serializers.CharField(max_length=16, required=False)
    eth_address = serializers.CharField(required=False)

    def validate_email(self, email_address):
        normalized_email_address = User.objects.normalize_email(email_address)
        if User.objects.filter(email__iexact=normalized_email_address).exists():
            raise serializers.ValidationError(self.error_messages['duplicate_email'])
        return normalized_email_address

    def validate(self, data):
        if not data['password1'] == data['password2']:
            raise serializers.ValidationError(self.error_messages['password_mismatch'])
        return data

    def create(self, validated_data):
        create_account_kwargs = {
            'email': validated_data['email'],
            'password': validated_data['password1']
        }
        if 'keybase_username' in validated_data:
            create_account_kwargs['keybase_username'] = validated_data['keybase_username']
        user = User.objects.create_user(**create_account_kwargs)

        create_settings_kwargs = {
            'user': user
        }
        if 'eth_address' in validated_data:
            create_settings_kwargs['rpc_node_host'] = validated_data['eth_address']
        AccountConfig.objects.create(**create_settings_kwargs)

        user.send_verification_email()
        return user


class VerifyKeybaseSerializer(serializers.Serializer):
    signed_message = serializers.CharField(write_only=True)
    keybase_username = serializers.CharField(write_only=True)

    def validate(self, data):
        if self.instance is None:
            raise serializers.ValidationError("Cannot verify without a user instance")

        if self.instance.keybase_username:
            raise serializers.ValidationError("Cannot override existing keybase username")

        public_key_provider = get_provider()
        public_key_pem = public_key_provider.get_public_key(data["keybase_username"])
        signed_message = data['signed_message']

        with gpg_keyring(public_key_pem) as gpg:
            verification = gpg.verify(signed_message)
            validate_signature(verification)

            message = gpg.decrypt(signed_message).data.strip()

        try:
            user_id = signing.loads(message, max_age=datetime.timedelta(minutes=10))
        except signing.SignatureExpired:
            raise serializers.ValidationError(
                "Token expired. Please refresh and generate a new one."
            )
        except signing.BadSignature:
            raise serializers.ValidationError(
                "Could not validate token. Make sure you copied "
                "the full token or refresh and try again."
            )

        if user_id != self.instance.id:
            raise serializers.ValidationError("Mismatched user ID")

        return data

    def update(self, instance, validated_data):
        instance.keybase_username = validated_data['keybase_username']
        instance.is_keybase_verified = True
        instance.save()
        return instance


class AccountConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountConfig
        fields = ('rpc_node_host',)


class AccountShortSerializer(serializers.ModelSerializer):
    """
    used for user actions
    """
    keybase_verified = serializers.BooleanField(source='is_keybase_verified')

    class Meta:
        model = User
        fields = ('keybase_username',
                  'keybase_verified',
                  'email')
        read_only_fields = ('keybase_verified',)

    def validate(self, attrs):
        if 'email' in attrs:
            self.instance.verified_at = None
        return super(AccountShortSerializer, self).validate(attrs)


class AccountDetailSerializer(serializers.ModelSerializer):
    """
    used for admin actions
    """
    staff = serializers.BooleanField(source='is_staff')
    superuser = serializers.BooleanField(source='is_superuser')
    active = serializers.BooleanField(source='is_active')
    risk_assessor = serializers.BooleanField(source='is_risk_assessor')
    email_verified = serializers.SerializerMethodField()
    keybase_verified = serializers.BooleanField(source='is_keybase_verified')

    class Meta:
        model = User
        fields = ('keybase_username',
                  'email',
                  'date_joined',
                  'last_login',
                  'verified_at',
                  'superuser',
                  'staff',
                  'active',
                  'risk_assessor',
                  'email_verified',
                  'id',
                  'keybase_verified'
                  )
        read_only_fields = ('id',
                            'date_joined',
                            'last_login')

    def get_email_verified(self, instance):
        if instance.verified_at:
            return True
        return False


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('keybase_username',
                  'email',
                  'id')


class AccountLoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)
