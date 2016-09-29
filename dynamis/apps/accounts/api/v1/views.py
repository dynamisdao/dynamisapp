from django.contrib.auth import (
    authenticate,
    login,
    get_user_model)
from rest_framework import (
    generics,
    permissions,
)
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from dynamis.apps.accounts.api.v1.serializers import AccountShortSerializer, AccountListSerializer
from dynamis.apps.accounts.permissions import AccountPermission, IsAdminOrAccountOwnerPermission
from dynamis.apps.payments.models import EthAccount
from dynamis.core.api.v1.filters import IsOwnerOrAdminFilterBackend
from dynamis.core.view_mixins import DynamisCreateModelMixin
from .serializers import (
    AccountCreationSerializer,
    VerifyKeybaseSerializer,
    EthAccountSerializer, AccountDetailSerializer)


User = get_user_model()


# TODO - deprecated
class AccountCreationAPIView(generics.CreateAPIView):
    serializer_class = AccountCreationSerializer

    def perform_create(self, serializer):
        serializer.save()
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password1'],
        )
        login(self.request, user)


# TODO - deprecated
class DEPR_ManualKeybaseVerificationView(generics.UpdateAPIView):
    serializer_class = VerifyKeybaseSerializer
    permissions_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ManualKeybaseVerificationViewSet(mixins.UpdateModelMixin,
                                       GenericViewSet):
    queryset = User.objects.all()
    serializer_class = VerifyKeybaseSerializer
    permission_classes = (IsAdminOrAccountOwnerPermission,)

    class Meta:
        model = User


class EthAccountViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    queryset = EthAccount.objects.all()
    filter_backends = (IsOwnerOrAdminFilterBackend,)
    permission_classes = [IsAuthenticated]
    serializer_class = EthAccountSerializer

    class Meta:
        model = EthAccount


class AccountViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     DynamisCreateModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):

    permission_classes = [AccountPermission]
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser, IsAuthenticated]
        self.check_permissions(request)
        self.serializer_class = AccountListSerializer
        return super(AccountViewSet, self).list(request, *args, **kwargs)

    def perform_create(self, serializer):
        super(AccountViewSet, self).perform_create(serializer)
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password1'],
        )
        login(self.request, user)

    def create(self, request, *args, **kwargs):
        self.serializer_class = AccountCreationSerializer
        return super(AccountViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.set_serializer_class_by_user(request.user)
        return super(AccountViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.set_serializer_class_by_user(request.user)
        kwargs['partial'] = True
        return super(AccountViewSet, self).update(request, *args, **kwargs)

    def set_serializer_class_by_user(self, user):
        if user.is_admin:
            self.serializer_class = AccountDetailSerializer
        else:
            self.serializer_class = AccountShortSerializer

    class Meta:
        model = User
