import datetime
import json

import pytest
from rest_framework.exceptions import ValidationError

from dynamis.apps.policy.models import EmploymentHistoryJob
from dynamis.apps.policy.validation import validate_policy_application
from dynamis.utils import testing
from dynamis.apps.policy.business_logic import convert_month_year_to_date, generate_employment_history_job_records


def test_convert_month_year_to_date():
    test_data = ('0', '1975')
    result = convert_month_year_to_date(*test_data)
    assert result == datetime.date(1975, 1, 31)


def test_convert_month_year_to_date_wrong_year():
    test_data = ('0', '75')
    with pytest.raises(ValidationError):
        result = convert_month_year_to_date(*test_data)


def test_convert_month_year_to_date_wrong_month():
    test_data = ('13', '1975')
    with pytest.raises(ValidationError):
        result = convert_month_year_to_date(*test_data)


def test_generate_employment_history_job_records_no_policy_data(factories):
    policy = factories.PolicyApplicationFactory()
    with pytest.raises(ValidationError) as excinfo:
        generate_employment_history_job_records(policy)
    assert excinfo.value.detail[0] == 'policy have no jobs in employmentHistory'


def test_generate_employment_history_job_records_incorrect_job_data(gpg_key, gpg, factories, api_client,
                                                                    user, policy_data, monkeypatch):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append({'dummy': 'data'})

    monkeypatch.setitem(testing.PROOF_DB, ('test',), policy_data['identity']['verification_data']['proofs'])

    # sanity check that we are using valid test data.
    validate_policy_application(policy_data)

    policy_application = factories.PolicyApplicationFactory(
        user=user,
        data=json.dumps(policy_data),
    )
    with pytest.raises(ValidationError) as excinfo:
        generate_employment_history_job_records(policy_application)
    assert excinfo.value.detail[0] == 'Incorrect job data'


def test_generate_employment_history_job_records_pk(gpg_key, gpg, factories, api_client,
                                                    user, policy_data, monkeypatch, job_data):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    monkeypatch.setitem(testing.PROOF_DB, ('test',), policy_data['identity']['verification_data']['proofs'])

    # sanity check that we are using valid test data.
    validate_policy_application(policy_data)

    policy_application = factories.PolicyApplicationFactory(
        user=user,
        data=json.dumps(policy_data),
    )
    generate_employment_history_job_records(policy_application)

    job_record = EmploymentHistoryJob.objects.get()
    assert job_record.user == policy_application.user
    assert job_record.policy == policy_application
    assert job_record.company == job_data['company']
    assert job_record.is_current_job == job_data['currentJob']
    assert job_record.notes == job_data['notes']
    assert job_record.state == job_data['state']
    assert job_record.date_begin.month == int(job_data['startMonth']) + 1
    assert job_record.date_begin.year == int(job_data['startYear'])
    assert job_record.date_end.month == int(job_data['endMonth']) + 1
    assert job_record.date_end.year == int(job_data['endYear'])
