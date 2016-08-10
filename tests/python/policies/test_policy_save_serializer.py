import json

from dynamis.apps.policy.api.v1.serializers import PolicyApplicationSerializer


def test_policy_application_serializer_create(user):
    data = {
        'data': {
            'test': 'This is some test data',
        },
    }
    serializer = PolicyApplicationSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    policy_application = serializer.save(user=user)

    assert policy_application.user == user
    assert policy_application.is_final is False
    assert json.loads(policy_application.data) == data['data']


def test_policy_application_serializer_update(factories):
    data = {
        'data': {
            'field-b': 'This is field B',
        },
    }
    policy_application = factories.PolicyApplicationFactory()
    serializer = PolicyApplicationSerializer(policy_application, data=data)

    assert serializer.is_valid(), serializer.errors

    saved_policy_application = serializer.save()

    assert json.loads(saved_policy_application.data) == data['data']


def test_policy_application_serializer_output(factories):
    policy_application = factories.PolicyApplicationFactory()
    serializer = PolicyApplicationSerializer(policy_application)

    data = serializer.data

    assert data['data'] == json.loads(policy_application.data)
