import django_tables2 as tables
from django_tables2 import A

from dynamis.apps.payments.models import SmartDeposit
from dynamis.apps.policy.models import RiskAssessmentTask
from dynamis.utils.tables import MaterializedTable


class SmartDepositTable(MaterializedTable):
    class Meta(MaterializedTable.Meta):
        model = SmartDeposit
        order_by = ('id',)
        fields = (
            'id',
            'amount',
            'is_confirmed'
        )


class RiskAssessmentTaskTable(MaterializedTable):
    policy = tables.LinkColumn('risk-assessment', args=(A('id'),))

    class Meta(MaterializedTable.Meta):
        model = RiskAssessmentTask
        order_by = ('-is_finished', 'id')
        fields = (
            'id',
            'policy',
            'is_finished',
        )