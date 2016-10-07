from constance import config

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer


def test_deposit_short_serializer(factories):
    deposit = factories.SmartDepositFactory()

    data = {
        'status': deposit.state,
        'coast_in_eth': deposit.coast,
        'coast_in_dollars': deposit.coast_dollar,
        'address_to_send': config.ADDRESS_TO_SEND_ETH
    }

    serializer = SmartDepositShortSerializer(instance=deposit)
    assert serializer.data == data
