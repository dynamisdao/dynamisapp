from django.views.generic import ListView
from django_tables2 import SingleTableMixin

from dynamis.apps.accounts._admin.tables import PolicyTable
from dynamis.apps.policy.models import PolicyApplication, POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED, \
    POLICY_STATUS_ON_P2P_REVIEW, POLICY_STATUS_ON_COMPLETENESS_CHECK, POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW
from dynamis.utils.mixins import (
    AdminRequired
)


class AdminIndexView(AdminRequired, SingleTableMixin, ListView):
    queryset = PolicyApplication.objects.filter(state__in=(POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED,
                                                           POLICY_STATUS_ON_P2P_REVIEW,
                                                           POLICY_STATUS_ON_COMPLETENESS_CHECK,
                                                           POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW))
    template_name = 'admin/admin_index.html'
    table_class = PolicyTable
    table_pagination = {
        'per_page': 20,
    }
