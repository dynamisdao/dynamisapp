import pytest

from dynamis.apps.accounts.api.v1.serializers import AccountCreationSerializer
from dynamis.apps.payments.models import EthAccount


def test_account_creation(User):
    data = {
        'email': 'test@Example.com',
        'password1': 'test-password',
        'password2': 'test-password',
    }
    serializer = AccountCreationSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    assert not User.objects.filter(email='test@example.com').exists()

    user = serializer.save()
    assert user.check_password('test-password')
    # see that the email address was normalized.
    assert user.email == 'test@example.com'
    assert EthAccount.objects.exists() is True


@pytest.mark.django_db
def test_mismatched_passwords():
    data = {
        'email': 'test@example.com',
        'password1': 'test-password-a',
        'password2': 'test-password-b',
    }
    serializer = AccountCreationSerializer(data=data)
    not serializer.is_valid()

    expected_msg = AccountCreationSerializer.default_error_messages['password_mismatch']

    assert expected_msg in serializer.errors['non_field_errors']


def test_duplicate_email_address(user):
    data = {
        'email': user.email,
        'password1': 'test-password',
        'password2': 'test-password',
    }
    serializer = AccountCreationSerializer(data=data)
    not serializer.is_valid()

    expected_msg = AccountCreationSerializer.default_error_messages['duplicate_email']

    assert expected_msg in serializer.errors['email']
