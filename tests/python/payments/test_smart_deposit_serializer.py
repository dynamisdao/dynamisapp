from constance import config

from dynamis.apps.payments.api.v1.serializers import SmartDepositShortSerializer


def test_deposit_short_serializer(factories):
    deposit = factories.SmartDepositFactory()

    data = {
        'status': deposit.state,
        'cost_in_eth': deposit.cost,
        'cost_in_wei': deposit.cost_wei,
        'cost_in_dollars': deposit.cost_dollar,
        'address_to_send': config.SYSTEM_ETH_ADDRESS
    }

    serializer = SmartDepositShortSerializer(instance=deposit)
    assert serializer.data == data
