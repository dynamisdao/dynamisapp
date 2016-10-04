import json
import itertools

from rest_framework import serializers

from dynamis.utils.gpg import gpg_keyring
from dynamis.utils.validation import (
    validate_signature,
    SIGNATURE_ERROR_MESSAGES,
)
from dynamis.apps.identity import get_provider
from dynamis.utils.ipfs import get_ipfs_client

from dynamis.apps.policy.models import (
    PolicyApplication,
    ReviewTask,
    PeerReview,
    RiskAssessmentTask)
from dynamis.apps.policy.validation import (
    validate_policy_application,
    validate_peer_review,
)


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return json.dumps(data, sort_keys=True)

    def to_representation(self, value):
        if value:
            return json.loads(value)


class PolicyApplicationSerializer(serializers.ModelSerializer):
    data = JSONSerializerField(required=False)

    class Meta:
        model = PolicyApplication
        fields = ('id', 'data', 'is_signed')
        read_only_fields = ('is_signed',)


class PolicySubmissionSerializer(serializers.ModelSerializer):
    default_error_messages = dict(itertools.chain(
        (
            ('json_invalid', 'Invalid message body'),
            ('proofs_invalid', 'Invalid proofs'),
        ),
        SIGNATURE_ERROR_MESSAGES.items()
    ))
    keybase_username = serializers.CharField(write_only=True)
    signed_message = serializers.CharField(write_only=True)

    class Meta:
        model = PolicyApplication
        fields = ('keybase_username', 'signed_message')

    def validate(self, data):
        keybase_username = data["keybase_username"]
        signed_message = data['signed_message']

        public_key_provider = get_provider()
        public_key_pem = public_key_provider.get_public_key(keybase_username)

        with gpg_keyring(public_key_pem) as gpg:
            verification = gpg.verify(signed_message)
            validate_signature(verification)

            message = gpg.decrypt(signed_message).data

        try:
            policy_data = json.loads(message)
        except ValueError:
            raise serializers.ValidationError(self.error_messages['json_invalid'])

        validate_policy_application(policy_data)

        expected_proofs = public_key_provider.get_proofs(keybase_username)
        actual_proofs = policy_data['identity']['verification_data']['proofs']

        expected_proofs_set = set(json.dumps(v, sort_keys=True) for v in expected_proofs)
        actual_proofs_set = set(json.dumps(v, sort_keys=True) for v in actual_proofs)

        if expected_proofs_set != actual_proofs_set:
            raise serializers.ValidationError(self.error_messages['proofs_invalid'])

        validated_data = {
            'is_final': True,
            'data': json.dumps({
                'policy_data': policy_data,
                'signed_message': signed_message,
                'public_key': public_key_pem,
                'public_key_provider': public_key_provider.name,
                'public_key_identity': {
                    'username': keybase_username,
                }
            }, sort_keys=True),
            'is_signed': True
        }
        return validated_data


class ApplicationItemSerializer(serializers.ModelSerializer):
    data = JSONSerializerField()

    class Meta:
        model = ReviewTask
        fields = ('id', 'type', 'data', 'is_finished')


class PeerReviewSubmissionSerializer(serializers.ModelSerializer):
    default_error_messages = dict(itertools.chain(
        (('json_invalid', 'Invalid message body'),),
        SIGNATURE_ERROR_MESSAGES.items()
    ))

    signed_message = serializers.CharField(write_only=True)

    class Meta:
        model = PeerReview
        fields = ('signed_message',)

    def __init__(self, *args, **kwargs):
        self.keybase_username = kwargs.pop('keybase_username')
        super(PeerReviewSubmissionSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        public_key_provider = get_provider()
        public_key_pem = public_key_provider.get_public_key(self.keybase_username)
        signed_message = data['signed_message']

        with gpg_keyring(public_key_pem) as gpg:
            verification = gpg.verify(signed_message)
            validate_signature(verification)

            message = gpg.decrypt(signed_message).data

        try:
            peer_review_data = json.loads(message)
        except ValueError:
            raise serializers.ValidationError(self.error_messages['json_invalid'])

        validate_peer_review(peer_review_data)

        validated_data = {
            'data': json.dumps({
                'policy_application': peer_review_data,
                'signed_message': signed_message,
                'public_key': public_key_pem,
                'public_key_provider': public_key_provider.name,
                'public_key_identity': {
                    'username': self.keybase_username,
                }
            }, sort_keys=True),
            'result': peer_review_data['result'],
        }

        return validated_data


class PeerReviewSerializer(serializers.ModelSerializer):
    application_item = ApplicationItemSerializer(read_only=True)

    class Meta:
        fields = ('id', 'application_item', 'user', 'data')
        model = PeerReview


class IPFSFileSerializer(serializers.Serializer):
    filename = serializers.CharField(write_only=True)
    mimetype = serializers.CharField(write_only=True)
    data_url = serializers.CharField(write_only=True)

    ipfs_hash = serializers.CharField(read_only=True)
    meta = serializers.DictField(read_only=True)

    def create(self, validated_data):
        ipfs_client = get_ipfs_client()
        ipfs_hash = ipfs_client.add_json(validated_data)
        return {
            'ipfs_hash': ipfs_hash,
            'meta': {
                'name': validated_data['filename'],
                'mimetype': validated_data['mimetype'],
            },
        }


class RiskAssessmentTaskDetailSerializer(serializers.ModelSerializer):
    policyid = serializers.IntegerField(source='policy.id', required=False, read_only=True)

    class Meta:
        model = RiskAssessmentTask
        fields = ('id', 'policyid', 'is_finished', 'bet1', 'bet2')


class RiskAssessmentTaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessmentTask
        fields = ('id', 'is_finished')
