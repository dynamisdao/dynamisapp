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


@pytest.fixture
def job_data():
    job_data = {
        'company': "test company",
        'currentJob': True,
        'endMonth': "0",
        'endYear': '2016',
        'notes': 'some notes',
        'startMonth': '3',
        'startYear': '2015',
        'state': 'READ_ONLY',
    }
    return job_data
