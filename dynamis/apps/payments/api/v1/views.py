from django.utils import timezone
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer
from dynamis.apps.payments.models import SmartDeposit
from dynamis.core.permissions import IsAdminOrPolicyOwnerPermission


class SmartDepositViewSet(mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SmartDepositShortSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrPolicyOwnerPermission)
    queryset = SmartDeposit.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.wait_for < timezone.now():
            instance.wait_to_init()
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
