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

from dynamis.apps.policy.business_logic import generate_review_tasks, generate_employment_history_job_records
from dynamis.apps.policy.models import (
    PolicyApplication,
    ReviewTask,
    PeerReview,
    RiskAssessmentTask, POLICY_STATUS_INIT, EmploymentHistoryJob)
from dynamis.core.api.v1.filters import IsOwnerOrAdminFilterBackend
from dynamis.core.permissions import IsAdminOrObjectOwnerPermission
from dynamis.core.view_mixins import DynamisCreateModelMixin

from .serializers import (
    PolicyApplicationSerializer,
    PolicySubmissionSerializer,
    ApplicationItemSerializer,
    PeerReviewSubmissionSerializer,
    PeerReviewSerializer,
    IPFSFileSerializer,
    RiskAssessmentTaskDetailSerializer, RiskAssessmentTaskShortSerializer)


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
        return policy

    @atomic
    def perform_update(self, serializer):
        serializer.save()
        policy = self.get_object()
        self.generate_employment_history_jobs(policy)

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
            return ValidationError('Policy already submited')

        serializer = PolicySubmissionSerializer(policy, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        submitted_policy = serializer.save()

        generate_review_tasks(submitted_policy)

        self.request.user.keybase_username = self.request.data["keybase_username"]
        self.request.user.save()
        messages.success(
            # messages framework requires we use the Django HTTPRequest object
            # instead of DRF's request object.
            self.request._request, "Policy #{0} has been submitted".format(submitted_policy.pk)
        )

        policy.submit()
        policy.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

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

    @detail_route(methods=['post'], url_path='verify')
    def verify(self, *args, **kwargs):
        application_item = self.get_object()
        serializer = PeerReviewSubmissionSerializer(
            data=self.request.data,
            keybase_username=self.request.user.get_keybase_username(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, application_item=application_item)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    serializer_class = RiskAssessmentTaskDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrObjectOwnerPermission)
    queryset = RiskAssessmentTask.objects.all()
    filter_backends = (IsOwnerOrAdminFilterBackend,)

    def list(self, request, *args, **kwargs):
        self.serializer_class = RiskAssessmentTaskShortSerializer
        return super(RiskAssessmentTaskViewSet, self).list(request, *args, **kwargs)
