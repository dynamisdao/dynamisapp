import itertools
import json

from dynamis.apps.policy.models import ApplicationItem


# TODO: This should be made idempotent as to not create duplicate application items in the event
#  that this is triggered twice.
def generate_application_items(policy_application):
        policy_data = json.loads(policy_application.data)['policy_data']
        identities = policy_data['identity']['verification_data']['proofs']
        employment_records = policy_data['employmentHistory']['jobs']

        identity_items = (
            {
                'policy_application_id': policy_application.pk,
                'type': ApplicationItem.TYPE_IDENTITY,
                'data': json.dumps(item),
            }
            for item in identities
        )
        employment_history_items = (
            {
                'policy_application_id': policy_application.pk,
                'type': ApplicationItem.TYPE_EMPLOYMENT_CLAIM,
                'data': json.dumps(item),
            }
            for item in employment_records
        )
        application_items = [
            ApplicationItem(**item)
            for item in itertools.chain(identity_items, employment_history_items)
            ]
        return ApplicationItem.objects.bulk_create(application_items)
