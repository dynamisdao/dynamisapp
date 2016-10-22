from constance import config
from django.utils import timezone
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer, SmartDepositSendSerializer
from dynamis.apps.payments.models import SmartDeposit, SMART_DEPOSIT_STATUS_RECEIVED, \
    SMART_DEPOSIT_STATUS_WAITING
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
            instance.cost_dollar = instance.cost * config.DOLLAR_ETH_EXCHANGE_RATE
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SmartDepositSendView(viewsets.GenericViewSet):
    serializer_class = SmartDepositSendSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrPolicyOwnerPermission)
    queryset = SmartDeposit.objects.all()

    def send(self, request, *args, **kwargs):
        smart_deposit = self.get_object()
        if smart_deposit.state == SMART_DEPOSIT_STATUS_RECEIVED:
            return Response(data={'non_field_errors': 'smart deposit already received'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=smart_deposit, data=request.data)
        serializer.is_valid(raise_exception=True)

        smart_deposit.from_address = serializer.validated_data['from_address']

        if smart_deposit.state == SMART_DEPOSIT_STATUS_WAITING:
            smart_deposit.wait_to_init()

        smart_deposit.init_to_wait()
        smart_deposit.save()

        return Response(status=status.HTTP_200_OK)
