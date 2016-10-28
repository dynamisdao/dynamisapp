from django.db.transaction import atomic
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer, SmartDepositSendSerializer, \
    TokenAccountShortSerializer, BuyTokenInSerializer
from dynamis.apps.payments.business_logic import check_transfers_change_model_states
from dynamis.apps.payments.models import SmartDeposit, WAIT_FOR_TX_STATUS_RECEIVED, \
    WAIT_FOR_TX_STATUS_WAITING, TokenAccount, BuyTokenOperation
from dynamis.core.permissions import IsAdminOrPolicyOwnerPermission, IsAdminOrObjectOwnerPermission, \
    IsRiskAssessorPermission


class SmartDepositViewSet(mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SmartDepositShortSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrPolicyOwnerPermission)
    queryset = SmartDeposit.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        smart_deposit = check_transfers_change_model_states(instance)
        serializer = self.get_serializer(smart_deposit)
        return Response(serializer.data)


class SmartDepositSendView(viewsets.GenericViewSet):
    serializer_class = SmartDepositSendSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrPolicyOwnerPermission)
    queryset = SmartDeposit.objects.all()

    def send(self, request, *args, **kwargs):
        smart_deposit = self.get_object()
        if smart_deposit.state == WAIT_FOR_TX_STATUS_RECEIVED:
            return Response(data={'non_field_errors': 'smart deposit already received'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=smart_deposit, data=request.data)
        serializer.is_valid(raise_exception=True)

        smart_deposit.from_address = serializer.validated_data['from_address']

        if smart_deposit.state == WAIT_FOR_TX_STATUS_WAITING:
            smart_deposit.wait_to_init()

        smart_deposit.init_to_wait()
        smart_deposit.save()

        return Response(status=status.HTTP_200_OK)


class TokenAccountViewSet(mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = TokenAccountShortSerializer
    permission_classes = (permissions.IsAuthenticated, IsRiskAssessorPermission, IsAdminOrObjectOwnerPermission)
    queryset = TokenAccount.objects.filter(disabled=False)
    lookup_field = 'user'

    def retrieve(self, request, *args, **kwargs):
        token_account = self.get_object()
        if token_account.buy_token_operations.filter(state=WAIT_FOR_TX_STATUS_WAITING).exists():
            buy_token_operation = token_account.buy_token_operations.filter(state=WAIT_FOR_TX_STATUS_WAITING)[0]
            check_transfers_change_model_states(buy_token_operation)
            token_account.refresh_from_db()
        serializer = self.get_serializer(token_account)
        return Response(serializer.data)


class BuyTokenView(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    serializer_class = BuyTokenInSerializer
    permission_classes = (permissions.IsAuthenticated, IsRiskAssessorPermission)
    queryset = BuyTokenOperation.objects.all()

    @atomic
    def perform_create(self, serializer):
        buy_operation = serializer.save()
        buy_operation.init_to_wait()
        buy_operation.save()

    def create(self, request, *args, **kwargs):
        if request.user.token_account.buy_token_operations.filter(state=WAIT_FOR_TX_STATUS_WAITING).exists():
            return Response(
                data={'non_field_errors': 'you try to buy token second time, we still wait for previous payment'},
                status=status.HTTP_400_BAD_REQUEST)

        request.data.update({'token_account': request.user.token_account.pk})
        return super(BuyTokenView, self).create(request, *args, **kwargs)
