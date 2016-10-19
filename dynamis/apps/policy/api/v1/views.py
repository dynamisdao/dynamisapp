from django.contrib import messages
from django.db.transaction import atomic

from rest_framework import (
    mixins,
    viewsets,
    permissions,
    status,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from dynamis.apps.accounts.models import User
from dynamis.apps.payments.models import TokenAccount, MakeBetOperation
from dynamis.apps.policy.business_logic import generate_employment_history_job_records, \
    set_answers_on_questions, calculate_and_set_smart_deposit_cost
from dynamis.apps.policy.models import (
    PolicyApplication,
    ReviewTask,
    PeerReview,
    RiskAssessmentTask, POLICY_STATUS_INIT, EmploymentHistoryJob)
from dynamis.core.api.v1.filters import IsOwnerOrAdminFilterBackend
from dynamis.core.permissions import IsAdminOrObjectOwnerPermission
from dynamis.core.view_mixins import DynamisCreateModelMixin
from dynamis.settings import DEBUG

from .serializers import (
    PolicyApplicationSerializer,
    PolicySubmissionSerializer,
    ApplicationItemSerializer,
    PeerReviewSubmissionSerializer,
    PeerReviewSerializer,
    IPFSFileSerializer,
    RiskAssessmentTaskDetailUserSerializer, RiskAssessmentTaskShortSerializer, RiskAssessmentTaskDetailAdminSerializer)


class PolicyApplicationViewSet(DynamisCreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = PolicyApplicationSerializer
    permissions_classes = (permissions.IsAuthenticated, IsAdminOrObjectOwnerPermission)
    queryset = PolicyApplication.objects.all()

    def list(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        self.check_permissions(request)
        return super(PolicyApplicationViewSet, self).list(request, *args, **kwargs)

    @atomic
    def perform_create(self, serializer):
        policy = serializer.save(user=self.request.user)
        self.generate_employment_history_jobs(policy)
        self.set_answers_on_questions(policy)
        calculate_and_set_smart_deposit_cost(policy)
        return policy

    @atomic
    def perform_update(self, serializer):
        policy = serializer.save()
        if policy.state != POLICY_STATUS_INIT:
            policy.cancel_submission()
            policy.save()
        self.generate_employment_history_jobs(policy)
        self.set_answers_on_questions(policy)
        calculate_and_set_smart_deposit_cost(policy)

    @staticmethod
    def set_answers_on_questions(policy):
        if policy.data:
            set_answers_on_questions(policy)

    @staticmethod
    def generate_employment_history_jobs(policy):
        EmploymentHistoryJob.objects.filter(policy=policy).delete()
        if policy.data:
            generate_employment_history_job_records(policy)

    @detail_route(methods=['post'])
    @atomic
    def submit(self, *args, **kwargs):
        policy = self.get_object()
        if policy.state != POLICY_STATUS_INIT:
            raise ValidationError('Policy already submited')

        serializer = PolicySubmissionSerializer(policy, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        submitted_policy = serializer.save()

        # TODO remove when old frontend will disabled
        calculate_and_set_smart_deposit_cost(policy)

        self.request.user.keybase_username = self.request.data["keybase_username"]
        self.request.user.save()
        messages.success(
            # messages framework requires we use the Django HTTPRequest object
            # instead of DRF's request object.
            self.request._request, "Policy #{0} has been submitted".format(submitted_policy.pk)
        )

        policy.submit()
        policy.save()
        # policy.smart_deposit.init_to_wait()
        # policy.smart_deposit.save()

        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='upload-file')
    def upload_file(self, *args, **kwargs):
        serializer = IPFSFileSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewTasksViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ApplicationItemSerializer
    queryset = ReviewTask.objects.none()
    permissions_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ReviewTask.objects.get_review_queue(self.request.user)

    # TODO Deprecated
    @detail_route(methods=['post'], url_path='submit-peer-review')
    def submit_peer_review(self, *args, **kwargs):
        return self.verify(*args, **kwargs)

    # TODO refactoring - when we will call this url twice - system will produce two PeerReview objects -
    # better to use get_or_create
    @atomic
    @detail_route(methods=['post'], url_path='verify')
    def verify(self, *args, **kwargs):
        review_task = self.get_object()
        serializer = PeerReviewSubmissionSerializer(
            data=self.request.data,
            keybase_username=self.request.user.get_keybase_username(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, application_item=review_task)

        review_task.is_finished = True
        review_task.save()

        policy = review_task.policy_application
        if not ReviewTask.objects.filter(policy_application=policy, is_finished=False).exists():
            if DEBUG:
                policy.p2p_review_to_completeness_check()
            policy.completeness_check_to_risk_assessment_review()
            policy.save()

        return Response(status=status.HTTP_200_OK)


class PeerReviewHistoryViewSet(mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = PeerReviewSerializer
    queryset = PeerReview.objects.none()
    permissions_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.peer_reviews.all()


class RiskAssessmentTaskViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = RiskAssessmentTaskDetailUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrObjectOwnerPermission)
    queryset = RiskAssessmentTask.objects.all()
    filter_backends = (IsOwnerOrAdminFilterBackend,)

    def list(self, request, *args, **kwargs):
        self.serializer_class = RiskAssessmentTaskShortSerializer
        return super(RiskAssessmentTaskViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.is_admin:
            self.serializer_class = RiskAssessmentTaskDetailAdminSerializer
        return super(RiskAssessmentTaskViewSet, self).update(request, *args, **kwargs)

    @atomic
    def perform_update(self, serializer):
        instance = serializer.save()
        amount = instance.bet1 + instance.bet2
        user_token_account = TokenAccount.objects.get(user=instance.user)

        internal_contractor = User.objects.get(internal_contractor=True)
        contractor_token_account, _ = TokenAccount.objects.get_or_create(user=internal_contractor)

        operation = MakeBetOperation.objects.create(risk_assessment_task=instance,
                                                    assessor_token_account=user_token_account,
                                                    internal_contractor_token_account=contractor_token_account,
                                                    amount=amount)

        user_token_account.immature_tokens_balance -= amount
        user_token_account.save()

        contractor_token_account.immature_tokens_balance += amount
        contractor_token_account.save()

        instance.is_finished = True
        instance.save()
