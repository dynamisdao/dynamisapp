from dynamis.utils.validation import load_json_schema


validate_policy_application = load_json_schema('policy-application', 'v1')


def validate_peer_review(data):
    """
    TODO: Apply peer review validation rules.
    """
    pass
