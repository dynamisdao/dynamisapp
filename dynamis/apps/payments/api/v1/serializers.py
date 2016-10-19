from constance import config
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from dynamis.apps.payments.models import SmartDeposit


class SmartDepositShortSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(source='state')
    cost_in_eth = serializers.FloatField(source='cost')
    cost_in_dollars = serializers.FloatField(source='cost_dollar')
    address_to_send = SerializerMethodField()

    def get_address_to_send(self, *args, **kwargs):
        return config.ADDRESS_TO_SEND_ETH

    class Meta:
        model = SmartDeposit
        fields = ('status', 'cost_in_eth', 'cost_in_dollars', 'address_to_send')
        read_only_fields = '__all__'


class SmartDepositSendSerializer(serializers.Serializer):
    amount_in_eth = serializers.FloatField()
    from_address = serializers.CharField(max_length=1023)

    def validate_amount_in_eth(self, value):
        if self.instance.cost and self.instance.cost == value:
            return value
        else:
            raise ValidationError('smart deposit cost is not equal with received amount')
