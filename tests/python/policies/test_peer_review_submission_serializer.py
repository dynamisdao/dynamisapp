import json

from dynamis.apps.policy.validation import validate_peer_review
from dynamis.apps.policy.api.v1.serializers import PeerReviewSubmissionSerializer


def test_peer_review_submission_with_valid_signature(gpg_key, gpg, factories, user):
    peer_review_data = {
        'field-a': 'This is field A',
        'field-b': 'This is field B',
        'result': '1',
    }
    application_item = factories.IdentityApplicationItemFactory()

    # sanity check that we are using valid test data.
    validate_peer_review(peer_review_data)

    data = {
        'signed_message': gpg.sign(json.dumps(peer_review_data, sort_keys=True)).data,
    }
    serializer = PeerReviewSubmissionSerializer(data=data, keybase_username='test')
    assert serializer.is_valid(), serializer.errors

    peer_review = serializer.save(user=user, application_item=application_item)

    assert peer_review.result == '1'


def test_peer_review_submission_with_invalid_signature(gpg_key,
                                                       generate_gpg_key, gpg,
                                                       factories):
    peer_review_data = {
        'field-a': 'This is field A',
        'field-b': 'This is field B',
        'result': '1',
    }

    # sanity check that we are using valid test data.
    validate_peer_review(peer_review_data)

    other_key = generate_gpg_key('wrong_username')

    data = {
        'signed_message': gpg.sign(json.dumps(peer_review_data, sort_keys=True), keyid=other_key.fingerprint).data,
    }

    serializer = PeerReviewSubmissionSerializer(data=data, keybase_username='test')

    assert not serializer.is_valid()
    assert serializer.error_messages['signature_invalid'] in serializer.errors['non_field_errors']
