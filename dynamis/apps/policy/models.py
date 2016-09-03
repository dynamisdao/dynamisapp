from __future__ import unicode_literals

import itertools
import json

from django.conf import settings
from django.db import models

from .query import ApplicationItemQueryset


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PolicyApplication(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='policies')
    is_final = models.BooleanField(default=False)
    is_signed = models.BooleanField(default=False)
    data = models.TextField()

    def generate_application_items(self):
        """
        TODO: This should be made idempotent as to not create duplicate
        application items in the event that this is triggered twice.
        """
        policy_data = json.loads(self.data)['policy_data']
        identities = policy_data['identity']['verification_data']['proofs']
        employment_records = policy_data['employmentHistory']['jobs']

        identity_items = (
            {
                'policy_application_id': self.pk,
                'type': ApplicationItem.TYPE_IDENTITY,
                'data': json.dumps(item),
            }
            for item in identities
        )
        employment_history_items = (
            {
                'policy_application_id': self.pk,
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


class ApplicationItem(TimestampModel):
    policy_application = models.ForeignKey('policy.PolicyApplication', related_name='items')

    TYPE_IDENTITY = 'identity'
    TYPE_EMPLOYMENT_CLAIM = 'employment-claim'
    TYPE_CHOICES = (
        ('Identity', TYPE_IDENTITY),
        ('Employement Claim', TYPE_EMPLOYMENT_CLAIM),
    )
    type = models.CharField(max_length=32, choices=TYPE_CHOICES, editable=False)

    data = models.TextField(editable=False)

    objects = ApplicationItemQueryset.as_manager()


class PeerReview(TimestampModel):
    application_item = models.ForeignKey('policy.ApplicationItem', related_name='peer_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='peer_reviews')

    data = models.TextField()

    # Intentional denormalization to allow querying
    #
    # identity records are rated null or 1-5 (as strings)
    # employment claims are rated null, 'verified', or 'falsified'
    result = models.CharField(null=True, max_length=32)

    class Meta:
        unique_together = (
            ('application_item', 'user'),
        )
