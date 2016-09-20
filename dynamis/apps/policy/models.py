from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import models
from django_fsm import transition, FSMIntegerField

from dynamis.apps.payments.models import SmartDeposit, PremiumPayment
from dynamis.core.models import TimestampModel
from .querysets import ApplicationItemQueryset

POLICY_STATUS_INIT = 1
POLICY_STATUS_SUBMITTED = 2
POLICY_STATUS_ON_P2P_REVIEW = 3
POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW = 4
POLICY_STATUS_APPROVED = 5
POLICY_STATUS_ON_SMART_DEPOSIT_REFUND = 6
POLICY_STATUS_DELETED = 7
POLICY_STATUS_ACTIVE = 8
POLICY_STATUS_WAIT_FOR_PREMIUM = 9

POLICY_STATUS = {
    (POLICY_STATUS_INIT, 'init'),
    (POLICY_STATUS_SUBMITTED, 'submitted_wait_for_deposit'),
    (POLICY_STATUS_ON_P2P_REVIEW, 'on_p2p_review'),
    (POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, 'on_risk_assessment_review'),
    (POLICY_STATUS_APPROVED, 'approved'),
    (POLICY_STATUS_ON_SMART_DEPOSIT_REFUND, 'on_smart_deposit_refund'),
    (POLICY_STATUS_DELETED, 'deleted'),
    (POLICY_STATUS_ACTIVE, 'active'),
    (POLICY_STATUS_WAIT_FOR_PREMIUM, 'wait_for_premium')
}


class PolicyApplication(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='policies')
    is_final = models.BooleanField(default=False)
    is_signed = models.BooleanField(default=False)
    data = models.TextField()
    rejected_count = models.PositiveSmallIntegerField(default=0)
    state = FSMIntegerField(default=POLICY_STATUS_INIT, protected=True, choices=POLICY_STATUS)

    def check_smart_deposit_refunded(self):
        if SmartDeposit.objects.filter(user=self.user, refunded=True, is_confirmed=True).exists():
            return True
        return False

    def check_smart_deposit(self):
        if SmartDeposit.objects.filter(user=self.user, refunded=False, is_confirmed=True).exists():
            return True
        return False

    def check_p2p_review(self):
        peer_reviews = PeerReview.objects.filter(application_item__policy_application__user=self.user)

        # TODO FIXME REFACTORING - separate different king of rates !!!!
        # TODO use IDENTITY_RECORDS_RATIO
        if peer_reviews.exists() and not peer_reviews.filter(result__in=('falsified', '1', '2')):
            return True
        return False

    def check_risk_assessment_review(self):
        risk_assessment_reviews = RiskAssessmentTask.objects.filter(policy__user=self.user)
        if risk_assessment_reviews.exists() and not risk_assessment_reviews.filter(is_finished=False):
            return True
        return False

    def check_premium_payment(self):

        # TODO use PREMIUM_PAYMENT_PERIODICITY
        time_to_pay = datetime.datetime.now() - datetime.timedelta(weeks=4)

        if PremiumPayment.objects.filter(user=self.user, created_at__gte=time_to_pay):
            return True
        return False

    def check_wait_for_premium_payment(self):

        # TODO use PREMIUM_PAYMENT_PERIODICITY
        time_to_pay = datetime.datetime.now() - datetime.timedelta(weeks=4)

        if not PremiumPayment.objects.filter(user=self.user, created_at__gte=time_to_pay):
            return True
        return False

    @transition(field=state, source=POLICY_STATUS_INIT, target=POLICY_STATUS_SUBMITTED)
    def submit(self):
        pass

    @transition(field=state, source=POLICY_STATUS_SUBMITTED, target=POLICY_STATUS_INIT)
    def cancel_submission(self):
        pass

    @transition(field=state, source='*', target=POLICY_STATUS_ON_SMART_DEPOSIT_REFUND,
                conditions=[check_smart_deposit])
    def to_deposit_refund(self):
        self.rejected_count += 1
        self.save()

    @transition(field=state, source=POLICY_STATUS_ON_SMART_DEPOSIT_REFUND,
                target=POLICY_STATUS_INIT, conditions=[check_smart_deposit_refunded])
    def deposit_refund_to_init(self):
        pass

    @transition(field=state, source=POLICY_STATUS_SUBMITTED, target=POLICY_STATUS_ON_P2P_REVIEW,
                conditions=[check_smart_deposit])
    def submit_to_p2p_review(self):
        pass

    @transition(field=state, source=POLICY_STATUS_ON_P2P_REVIEW,
                target=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, conditions=[check_p2p_review])
    def p2p_review_to_risk_assessment_review(self):
        pass

    @transition(field=state, source=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                target=POLICY_STATUS_APPROVED, conditions=[check_risk_assessment_review])
    def risk_assessment_review_to_approved(self):
        pass

    @transition(field=state, source='*',
                target=POLICY_STATUS_ACTIVE, conditions=[check_premium_payment, check_risk_assessment_review,
                                                         check_p2p_review, check_smart_deposit])
    def activate(self):
        pass

    @transition(field=state, source='*',
                target=POLICY_STATUS_WAIT_FOR_PREMIUM, conditions=[check_wait_for_premium_payment])
    def wait_for_payment(self):
        pass


class ApplicationItem(TimestampModel):
    policy_application = models.ForeignKey('policy.PolicyApplication', related_name='items')
    is_finished = models.BooleanField(default=False)

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

    # TODO FIXME REFACTORING - separate different king of rates !!!!
    result = models.CharField(null=True, max_length=32)

    class Meta:
        unique_together = (
            ('application_item', 'user'),
        )


class RiskAssessmentTask(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='risk_assessment_task')
    policy = models.ForeignKey(PolicyApplication, related_name='risk_assessment_task')
    is_finished = models.BooleanField(default=False)
    bet1 = models.FloatField(null=True)
    bet2 = models.FloatField(null=True)
