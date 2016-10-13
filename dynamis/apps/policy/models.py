from __future__ import unicode_literals

import ast
import datetime
import itertools
import json

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_fsm import transition, FSMIntegerField

from dynamis.apps.payments.models import SmartDeposit, PremiumPayment, SmartDepositRefund, EthAccount
from dynamis.apps.accounts.models import User
from dynamis.core.models import TimestampModel
from constance import config

from dynamis.settings import DEBUG
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
POLICY_STATUS_ON_COMPLETENESS_CHECK = 10

POLICY_STATUS = (
    (POLICY_STATUS_INIT, 'init'),
    (POLICY_STATUS_SUBMITTED, 'submitted'),
    (POLICY_STATUS_ON_P2P_REVIEW, 'on_p2p_review'),
    (POLICY_STATUS_ON_COMPLETENESS_CHECK, 'on_completeness_check'),
    (POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, 'on_risk_assessment_review'),
    (POLICY_STATUS_APPROVED, 'approved'),
    (POLICY_STATUS_ON_SMART_DEPOSIT_REFUND, 'on_smart_deposit_refund'),
    (POLICY_STATUS_DELETED, 'deleted'),
    (POLICY_STATUS_ACTIVE, 'active'),
    (POLICY_STATUS_WAIT_FOR_PREMIUM, 'wait_for_premium')
)

LESS_THAN_YEAR = 0
IN_ABOUT_YEAR = 1
BEFORE_THE_END_OF_NEXT_YEAR = 2
MAYBE_BEFORE_TWO_YEARS_TIME = 3
MORE_THAN_TWO_YEARS = 4
I_LOVE_MY_JOB = 5

HOW_LONG_STAY_ANSWER_CHOICES = (
    (LESS_THAN_YEAR, "Less than 1 year"),
    (IN_ABOUT_YEAR, "In about 1 year"),
    (BEFORE_THE_END_OF_NEXT_YEAR, "Before the end of next year"),
    (MAYBE_BEFORE_TWO_YEARS_TIME, "Maybe before 2 years time"),
    (MORE_THAN_TWO_YEARS, "More than 2 years"),
    (I_LOVE_MY_JOB, "I love my job. I will work for my present employer till the day I die."),
)

ONE_TO_TWO_WEEKS = 0
THREE_WEEKS_TO_MONTH = 1
ONE_TO_TWO_MONTHS = 2
TWO_TO_THREE_MONTHS = 3
THREE_TO_FOUR_MONTHS = 4
MORE_THAN_FOUR_MONTHS = 5

UNEMPLOYMENT_PERIOD_ANSWER_CHOICES = (
    (ONE_TO_TWO_WEEKS, "About 1 to 2 weeks"),
    (THREE_WEEKS_TO_MONTH, "Maybe 3 weeks to 1 month"),
    (ONE_TO_TWO_MONTHS, "Perhaps 1 to 2 months"),
    (TWO_TO_THREE_MONTHS, "Possibly 2 to 3 months"),
    (THREE_TO_FOUR_MONTHS, "Potentially 3 to 4 months"),
    (MORE_THAN_FOUR_MONTHS, "I will need more than 4 months of coverage."),

)


class PolicyApplication(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='policies')
    is_final = models.BooleanField(default=False)
    is_signed = models.BooleanField(default=False)
    is_completeness_checked = models.BooleanField(default=False)
    data = models.TextField()
    rejected_count = models.PositiveSmallIntegerField(default=0)
    state = FSMIntegerField(default=POLICY_STATUS_INIT, protected=True, choices=POLICY_STATUS)
    how_long_stay_answer = models.PositiveSmallIntegerField(choices=HOW_LONG_STAY_ANSWER_CHOICES, null=True)
    unemployment_period_answer = models.PositiveSmallIntegerField(choices=UNEMPLOYMENT_PERIOD_ANSWER_CHOICES, null=True)

    def __unicode__(self):
        return "%s's %s" % (self.user.get_full_name(), 'policy')

    def check_smart_deposit_refunded(self):
        smart_deposits = SmartDeposit.objects.filter(policy=self)
        if smart_deposits.exists() and SmartDepositRefund.objects.filter(smart_deposit=smart_deposits[0]).exists():
            return True
        return False

    def check_smart_deposit(self):
        smart_deposits = SmartDeposit.objects.filter(policy=self)
        if smart_deposits.exists() and \
                not SmartDepositRefund.objects.filter(smart_deposit=smart_deposits[0]).exists() and \
                        smart_deposits[0].amount >= smart_deposits[0].coast:
            return True
        return False

    def check_smart_for_refund(self):
        smart_deposits = SmartDeposit.objects.filter(policy=self)
        if smart_deposits.exists() and \
                not SmartDepositRefund.objects.filter(smart_deposit=smart_deposits[0]).exists():
            return True
        return False

    def check_p2p_review(self):
        peer_reviews = PeerReview.objects.filter(application_item__policy_application__user=self.user)

        # TODO FIXME REFACTORING - separate different kinds of rates !!!!
        not_success_status_list = [str(i) for i in xrange(1, config.IDENTITY_RECORDS_RATIO)]
        not_success_status_list += ['falsified']
        if peer_reviews.exists() and not peer_reviews.filter(result__in=not_success_status_list):
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
        eth_accounts = EthAccount.objects.filter(user=self.user)
        if PremiumPayment.objects.filter(eth_account__in=eth_accounts, created_at__gte=time_to_pay):
            return True
        return False

    def check_wait_for_premium_payment(self):

        # TODO use PREMIUM_PAYMENT_PERIODICITY
        time_to_pay = datetime.datetime.now() - datetime.timedelta(weeks=4)

        eth_accounts = EthAccount.objects.filter(user=self.user)
        if not PremiumPayment.objects.filter(eth_account__in=eth_accounts, created_at__gte=time_to_pay):
            return True
        return False

    def check_is_completeness_checked(self):
        # TODO remove 'if debug' when we complete develop and will test all states
        if DEBUG:
            return True
        return self.is_completeness_checked

    @transition(field=state, source=POLICY_STATUS_INIT, target=POLICY_STATUS_SUBMITTED)
    def submit(self):
        pass

    @transition(field=state, source=POLICY_STATUS_SUBMITTED, target=POLICY_STATUS_INIT)
    def cancel_submission(self):
        pass

    @transition(field=state, source='*', target=POLICY_STATUS_ON_SMART_DEPOSIT_REFUND,
                conditions=[check_smart_for_refund])
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

        # TODO: This should be made idempotent as to not create duplicate application items in the event
        #  that this is triggered twice.
        policy_data = json.loads(self.data)['policy_data']
        identities = policy_data['identity']['verification_data']['proofs']
        employment_records = policy_data['employmentHistory']['jobs']

        identity_items = (
            {
                'policy_application_id': self.pk,
                'type': ReviewTask.TYPE_IDENTITY,
                'data': json.dumps(item),
            }
            for item in identities
        )
        employment_history_items = (
            {
                'policy_application_id': self.pk,
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

    @transition(field=state, source=POLICY_STATUS_ON_P2P_REVIEW,
                target=POLICY_STATUS_ON_COMPLETENESS_CHECK, conditions=[check_p2p_review])
    def p2p_review_to_completeness_check(self):

        # TODO I have to ensure about it and compare with business-logic
        assessment_tasks_count = RiskAssessmentTask.objects.filter(policy=self).count()
        if assessment_tasks_count >= config.RISK_ASSESSORS_PER_POLICY_COUNT:
            return

        assessors_count = User.objects.filter(is_risk_assessor=True).exclude(
            pk=self.user.pk).count()
        tasks_to_create_count = config.RISK_ASSESSORS_PER_POLICY_COUNT if \
            assessors_count >= config.RISK_ASSESSORS_PER_POLICY_COUNT else assessors_count

        assessors = User.objects.filter(is_risk_assessor=True).exclude(
            pk=self.user.pk).order_by('?')[:tasks_to_create_count]
        for assessor in assessors:
            RiskAssessmentTask.objects.create(policy=self, user=assessor)

    @transition(field=state, source=POLICY_STATUS_ON_COMPLETENESS_CHECK,
                target=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                conditions=[check_is_completeness_checked])
    def completeness_check_to_risk_assessment_review(self):
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


class ReviewTask(TimestampModel):
    policy_application = models.ForeignKey('policy.PolicyApplication', related_name='review_tasks')
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
    application_item = models.ForeignKey('policy.ReviewTask', related_name='peer_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='peer_reviews')

    data = models.TextField()

    # Intentional denormalization to allow querying
    #
    # identity records are rated null or 1-5 (as strings)
    # employment claims are rated null, 'verified', or 'falsified'

    # TODO FIXME REFACTORING - separate different kinds of rates !!!!
    result = models.CharField(null=True, max_length=32)

    class Meta:
        unique_together = (
            ('application_item', 'user'),
        )


class RiskAssessmentTask(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='risk_assessment_tasks')
    policy = models.ForeignKey(PolicyApplication, related_name='risk_assessment_tasks')
    is_finished = models.BooleanField(default=False)
    bet1 = models.FloatField(null=True)
    question1 = models.PositiveSmallIntegerField(null=True,
                                                 help_text='How many months will this policyholder pay in premiums'
                                                           ' before opening a claim?')
    bet2 = models.FloatField(null=True)
    question2 = models.FloatField(null=True,
                                  help_text='How many weeks will this policyholder recieve in payments before '
                                            'closing a claim? ')


class EmploymentHistoryJob(TimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='employment_history_jobs')
    policy = models.ForeignKey(PolicyApplication, related_name='employment_history_jobs')
    notes = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255)

    # TODO set as not null field
    city = models.CharField(blank=True, null=True, max_length=255)

    # TODO set as not null field
    job_titile = models.CharField(blank=True, null=True, max_length=255)

    # TODO set as not null field ?
    confirmer_email = models.EmailField(blank=True, max_length=255)

    # TODO set as not null field ?
    confirmer_name = models.CharField(blank=True, null=True, max_length=255)

    is_current_job = models.BooleanField()
    state = models.CharField(blank=True, null=True, max_length=255)
    date_begin = models.DateField()
    date_end = models.DateField(null=True)
