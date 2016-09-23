from dynamis.apps.payments.models import SmartDeposit
from dynamis.utils.tables import MaterializedTable


class SmartDepositTable(MaterializedTable):

    class Meta(MaterializedTable.Meta):
        model = SmartDeposit
        order_by = ('id',)
        fields = (
            'id',
            'amount',
            'is_confirmed',
        )
