from constance import config
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from dynamis.apps.payments.models import SmartDeposit, TokenAccount, BuyTokenOperation
from dynamis.utils.math import approximately_equal


class SmartDepositShortSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(source='state')
    cost_in_eth = serializers.FloatField(source='cost')
    cost_in_wei = serializers.FloatField(source='cost_wei')
    cost_in_dollars = serializers.FloatField(source='cost_dollar')
    address_to_send = SerializerMethodField()

    def get_address_to_send(self, *args, **kwargs):
        return config.SYSTEM_ETH_ADDRESS

    class Meta:
        model = SmartDeposit
        fields = ('status', 'cost_in_eth', 'cost_in_dollars', 'address_to_send', 'cost_in_wei')
        read_only_fields = '__all__'


class SmartDepositSendSerializer(serializers.Serializer):
    amount_in_wei = serializers.FloatField()
    from_address = serializers.CharField(max_length=1023)

    def validate_amount_in_wei(self, value):
        if self.instance.cost and approximately_equal(self.instance.cost_wei, value, config.TX_VALUE_DISPERSION):
            return value
        else:
            raise ValidationError('smart deposit cost is not equal with received amount')


class TokenAccountShortSerializer(serializers.ModelSerializer):
    address_to_send = SerializerMethodField()
    immature_token_cost = SerializerMethodField()
    status = SerializerMethodField()

    def get_address_to_send(self, instance):
        return config.SYSTEM_ETH_ADDRESS

    def get_immature_token_cost(self, instance):
        return config.EHT_TOKEN_EXCHANGE_RATE

    def get_status(self, instance):
        if instance.buy_token_operations.exists():
            return instance.buy_token_operations.last().state
        else:
            return None

    class Meta:
        model = TokenAccount
        fields = ('address_to_send', 'immature_token_cost', 'status')


class BuyTokenInSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    from_address = serializers.CharField(max_length=1023)

    class Meta:
        model = BuyTokenOperation
