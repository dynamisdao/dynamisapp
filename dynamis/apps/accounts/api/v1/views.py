from django.contrib.auth import (
    authenticate,
    login,
)

from rest_framework import (
    generics,
    permissions,
)

from .serializers import (
    AccountCreationSerializer,
    VerifyKeybaseSerializer,
)


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
