import pytest


@pytest.fixture
def policy_data():
    policy_data = {
        'identity': {
            "verification_method": "keybase",
            "verification_data": {
                "username": "test",
                "proofs": [],
            },
        },
        'employmentHistory': {
            'jobs': [],
        }
    }
    return policy_data
