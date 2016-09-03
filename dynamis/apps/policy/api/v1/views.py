from django.contrib import messages

from rest_framework import (
    mixins,
    viewsets,
    permissions,
    status,
)
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from dynamis.apps.policy.models import (
    PolicyApplication,
    ApplicationItem,
    PeerReview,
)
from dynamis.core.permissions import IsAdminOrObjectOwnerPermission

from .serializers import (
    PolicyApplicationSerializer,
    PolicySubmissionSerializer,
    ApplicationItemSerializer,
    PeerReviewSubmissionSerializer,
    PeerReviewSerializer,
    IPFSFileSerializer,
)


class PolicyApplicationViewSet(mixins.CreateModelMixin,
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

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @detail_route(methods=['post'])
    def submit(self, *args, **kwargs):
        instance = self.get_object()
        serializer = PolicySubmissionSerializer(instance, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        policy_application = serializer.save()
        policy_application.generate_application_items()
        self.request.user.keybase_username = self.request.data["keybase_username"]
        self.request.user.save()
        messages.success(
            # messages framework requires we use the Django HTTPRequest object
            # instead of DRF's request object.
            self.request._request, "Policy #{0} has been submitted".format(policy_application.pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'], url_path='upload-file')
    def upload_file(self, *args, **kwargs):
        serializer = IPFSFileSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ApplicationItemReviewQueueViewSet(mixins.ListModelMixin,
                                        viewsets.GenericViewSet):
    serializer_class = ApplicationItemSerializer
    queryset = ApplicationItem.objects.none()
    permissions_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ApplicationItem.objects.get_review_queue(self.request.user)

    @detail_route(methods=['post'], url_path='submit-peer-review')
    def submit_peer_review(self, *args, **kwargs):
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
