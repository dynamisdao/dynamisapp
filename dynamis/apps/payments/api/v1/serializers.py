from constance import config
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from dynamis.apps.payments.models import SmartDeposit


class SmartDepositShortSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(source='state')
    coast_in_eth = serializers.FloatField(source='coast')
    coast_in_dollars = serializers.FloatField(source='coast_dollar')
    address_to_send = SerializerMethodField()

    def get_address_to_send(self, *args, **kwargs):
        return config.ADDRESS_TO_SEND_ETH

    class Meta:
        model = SmartDeposit
        fields = ('status', 'coast_in_eth', 'coast_in_dollars', 'address_to_send')
        read_only_fields = '__all__'
