import os
import json
import functools
import datetime

from jsonschema import validate

from rest_framework import serializers


def load_json_schema(schema_type, version):
    import dynamis

    filename = "{version}.json".format(version=version)
    path = os.path.join(
        os.path.dirname(dynamis.__file__), 'static', 'schema', schema_type, filename,
    )

    with open(path) as schema_file:
        schema = json.load(schema_file)

    validator = functools.partial(validate, schema=schema)
    return validator


SIGNATURE_EXPIRATION_DURATION = datetime.timedelta(minutes=30)
SIGNATURE_DRIFT_ALLOWANCE = datetime.timedelta(minutes=5)
SIGNATURE_ERROR_MESSAGES = {
    'signature_invalid': (
        'The signature could not be verified.  Please check that the '
        'message was signed with the appropriate public key'
    ),
    'signature_expired': (
        'The signature is to old.  Please re-sign and re-submit'
    ),
    'signature_from_future': (
        'The signature timestamp is invalid.  Check your system clock is '
        'correct'
    ),
}


def validate_signature(verification,
                       max_age=SIGNATURE_EXPIRATION_DURATION,
                       max_drift=SIGNATURE_DRIFT_ALLOWANCE):
    """
    Takes the `verification` object returned from `gpg.verify(...)` and
    validates:
        * signature is valid
        * not older than `max_age`
        * not more than `max_drift` in the future.
    """
    if not verification.valid:
        raise serializers.ValidationError(
            SIGNATURE_ERROR_MESSAGES['signature_invalid']
        )

    # timezone in production server should be utc
    time_now = datetime.datetime.now()
    time_signed = datetime.datetime.fromtimestamp(float(verification.sig_timestamp))
    time_since_signed = time_now - time_signed

    if max_age is not None:
        if time_since_signed > max_age:
            raise serializers.ValidationError(
                SIGNATURE_ERROR_MESSAGES['signature_expired']
            )

    if max_drift is not None:
        if time_now + max_drift < time_signed:
            raise serializers.ValidationError(
                SIGNATURE_ERROR_MESSAGES['signature_from_future']
            )
