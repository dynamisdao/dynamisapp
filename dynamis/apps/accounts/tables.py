import django_tables2 as tables
from django_tables2 import A

from dynamis.apps.payments.models import SmartDeposit
from dynamis.apps.policy.models import RiskAssessmentTask
from dynamis.utils.tables import MaterializedTable


class SmartDepositTable(MaterializedTable):
    cost = tables.Column(verbose_name='amount, ETH')
    cost_dollar = tables.Column(verbose_name='amount, USD')
    exchange_rate_at_invoice_time = tables.Column(verbose_name='current exchange rate')
    amount = tables.Column(verbose_name='amount received')
    policy_state = tables.Column(verbose_name='policy state', accessor='policy.state')

    class Meta(MaterializedTable.Meta):
        model = SmartDeposit
        order_by = ('policy_id',)
        fields = (
            'policy_id',
            'amount',
            'cost',
            'cost_dollar',
            'exchange_rate_at_invoice_time',
            'state',
            'policy_state',
            'wait_for'
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
