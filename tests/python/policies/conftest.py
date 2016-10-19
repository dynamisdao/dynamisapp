import pytest


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


@pytest.fixture
def job_data_extended():
    job_data = {
        'company': "test company",
        'currentJob': True,
        'endMonth': "0",
        'endYear': '2016',
        'notes': 'some notes',
        'startMonth': '3',
        'startYear': '2015',
        'state': 'READ_ONLY',
        'city': 'SPB',
        'confirmerEmail': 'email@example.com',
        'confirmerName': 'Mr. Confirmer',
        'jobTitile': 'developer'
    }
    return job_data


@pytest.fixture
def questions_data():
    questions_data = {
        'howLongStay': 0,
        'unemploymentPeriod': 2
    }
    return questions_data
