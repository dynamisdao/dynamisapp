import json

from dynamis.apps.policy.validation import validate_policy_application
from dynamis.apps.policy.api.v1.serializers import PolicySubmissionSerializer

from dynamis.utils import testing


def test_policy_submission_with_valid_data(gpg_key, gpg, factories, policy_data):
    # sanity check that we are using valid test data.
    validate_policy_application(policy_data)

    policy_application = factories.PolicyApplicationFactory(data=json.dumps(policy_data))

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(policy_application.data).data,
    }
    serializer = PolicySubmissionSerializer(policy_application, data=data)
    assert serializer.is_valid(), serializer.errors

    assert policy_application.is_final is False

    saved_policy_application = serializer.save()

    assert saved_policy_application.pk == policy_application.pk
    assert saved_policy_application.is_final is True


def test_policy_submission_with_invalid_signature(gpg_key, generate_gpg_key,
                                                  gpg, factories, policy_data):
    # sanity check that we are using valid test data.
    validate_policy_application(policy_data)

    policy_application = factories.PolicyApplicationFactory(data=json.dumps(policy_data))
    other_key = generate_gpg_key('wrong_username')

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(policy_application.data, keyid=other_key.fingerprint).data,
    }
    serializer = PolicySubmissionSerializer(policy_application, data=data)
    assert not serializer.is_valid()
    assert serializer.error_messages['signature_invalid'] in serializer.errors['non_field_errors']


def test_policy_submission_with_out_of_order_proofs(gpg_key, gpg, factories,
                                                    policy_data, monkeypatch):
    proof_a = {
        'field-a': 'x',
        'field-b': 'y',
    }
    proof_b = {
        'field-a': '1',
        'field-b': '2',
    }
    policy_data['identity']['verification_data']['proofs'] = [proof_a, proof_b]
    monkeypatch.setitem(testing.PROOF_DB, ('test',), [proof_b, proof_a])

    # sanity check that we are using valid test data.
    validate_policy_application(policy_data)

    policy_application = factories.PolicyApplicationFactory(data=json.dumps(policy_data))

    data = {
        'keybase_username': 'test',
        'signed_message': gpg.sign(policy_application.data).data,
    }
    serializer = PolicySubmissionSerializer(policy_application, data=data)
    assert serializer.is_valid(), serializer.errors
