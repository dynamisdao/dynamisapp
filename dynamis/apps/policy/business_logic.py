import itertools
import json
import datetime
import calendar

from rest_framework.exceptions import ValidationError

from dynamis.apps.policy.models import ReviewTask, EmploymentHistoryJob, HOW_LONG_STAY_ANSWER_CHOICES, \
    UNEMPLOYMENT_PERIOD_ANSWER_CHOICES


# TODO: This should be made idempotent as to not create duplicate application items in the event
#  that this is triggered twice.
def generate_review_tasks(policy_application):
    policy_data = json.loads(policy_application.data)['policy_data']
    identities = policy_data['identity']['verification_data']['proofs']
    employment_records = policy_data['employmentHistory']['jobs']

    identity_items = (
        {
            'policy_application_id': policy_application.pk,
            'type': ReviewTask.TYPE_IDENTITY,
            'data': json.dumps(item),
        }
        for item in identities
    )
    employment_history_items = (
        {
            'policy_application_id': policy_application.pk,
            'type': ReviewTask.TYPE_EMPLOYMENT_CLAIM,
            'data': json.dumps(item),
        }
        for item in employment_records
    )
    application_items = [
        ReviewTask(**item)
        for item in itertools.chain(identity_items, employment_history_items)
        ]
    return ReviewTask.objects.bulk_create(application_items)


def convert_month_year_to_date(month, year):
    """
    :type month: str
    :type year: str
    :rtype: datetime.date
    """
    # TODO we have to change convention with frontend about month numbers, Jan isn't - 0, Jan is first!
    month_numb = int(month) + 1
    year_numb = int(year)
    try:
        month_abbr = calendar.month_abbr[month_numb]
    except IndexError:
        raise ValidationError('Incorrect month number')

    _, last_day_of_month = calendar.monthrange(year_numb, month_numb)

    try:
        return datetime.datetime.strptime('{} {} {} 00:00'.format(month_abbr, last_day_of_month, year_numb),
                                          '%b %d %Y %M:%S').date()
    except ValueError:
        raise ValidationError('Incorrect year')


def generate_employment_history_job_records(policy_application):
    policy_data = json.loads(policy_application.data)

    try:
        employment_records = policy_data['employmentHistory']['jobs']
    except KeyError:
        raise ValidationError('policy have no jobs in employmentHistory')

    for job_record in employment_records:
        try:
            data_to_create = {
                'policy': policy_application,
                'user': policy_application.user,
                'company': job_record['company'],
                'is_current_job': job_record['currentJob'],
                'notes': job_record['notes'],
                'state': job_record['state'],
                'date_begin': convert_month_year_to_date(job_record['startMonth'], job_record['startYear']),
                'date_end': (convert_month_year_to_date(job_record['endMonth'], job_record['endYear'])
                             if job_record.get('startYear') and job_record.get('startMonth') else None)

            }
        except KeyError:
            raise ValidationError('Incorrect job data')
        kwargs_to_update = {}

        if 'city' in job_record:
            kwargs_to_update.update({'city': job_record['city']})
        if 'confirmerEmail' in job_record:
            kwargs_to_update.update({'confirmer_email': job_record['confirmerEmail']})
        if 'confirmerName' in job_record:
            kwargs_to_update.update({'confirmer_name': job_record['confirmerName']})
        if 'jobTitile' in job_record:
            kwargs_to_update.update({'job_titile': job_record['jobTitile']})

        data_to_create.update(kwargs_to_update)

        EmploymentHistoryJob.objects.create(**data_to_create)


def set_answers_on_questions(policy_application):
    policy_data = json.loads(policy_application.data)

    # TODO remove default 0 when old frontend will disabled
    try:
        how_long_stay_answer = HOW_LONG_STAY_ANSWER_CHOICES[policy_data['questions']['howLongStay']][0]
    except (KeyError, IndexError):
        how_long_stay_answer = 0

    try:
        unemployment_period_answer = UNEMPLOYMENT_PERIOD_ANSWER_CHOICES[
            policy_data['questions']['unemploymentPeriod']][0]
    except (KeyError, IndexError):
        unemployment_period_answer = 0

    policy_application.how_long_stay_answer = how_long_stay_answer
    policy_application.unemployment_period_answer = unemployment_period_answer
    policy_application.save()
