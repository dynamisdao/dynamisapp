from django.contrib.auth import (
    authenticate,
    login,
)

from rest_framework import (
    generics,
    permissions,
)
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from dynamis.apps.accounts.api.v1.filters import UserFilterBackend
from dynamis.apps.accounts.models import AccountConfig
from .serializers import (
    AccountCreationSerializer,
    VerifyKeybaseSerializer,
    AccountConfigSerializer)


class AccountCreationAPIView(generics.CreateAPIView):
    serializer_class = AccountCreationSerializer

    def perform_create(self, serializer):
        serializer.save()
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password1'],
        )
        login(self.request, user)


class ManualKeybaseVerificationView(generics.UpdateAPIView):
    serializer_class = VerifyKeybaseSerializer
    permissions_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AccountConfigViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           GenericViewSet):

    queryset = AccountConfig.objects.all()
    filter_backends = (UserFilterBackend,)
    permission_classes = [IsAuthenticated]
    serializer_class = AccountConfigSerializer
    lookup_field = 'user__keybase_username'

    class Meta:
        model = AccountConfig
