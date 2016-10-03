from django.views.generic import RedirectView
from django.views.generic import (
    TemplateView,
    DetailView,
    FormView, ListView)
from django_tables2 import SingleTableMixin

from dynamis.apps.accounts.forms import SmartDepositStubForm
from dynamis.apps.accounts.tables import SmartDepositTable
from dynamis.apps.payments.models import SmartDeposit
from dynamis.apps.policy.models import POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED, PolicyApplication

from dynamis.utils.mixins import LoginRequired


class PolicyCreateView(DetailView):
    template_name = "policies/policy_create.html"
    context_object_name = "policy"

    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.policies.first()
        else:
            return None


class PolicyEditView(LoginRequired, DetailView):
    template_name = "policies/policy_create.html"
    context_object_name = "policy"

    def get_object(self):
        return self.request.user.policies.get(pk=self.kwargs['pk'])


class PeerReviewItemsView(LoginRequired, TemplateView):
    template_name = "policies/peer_review.html"


class SmartDepositStubView(LoginRequired, SingleTableMixin, FormView, ListView):
    template_name = "accounts/smart-deposit-stub.html"
    form_class = SmartDepositStubForm
    table_class = SmartDepositTable
    success_url = '/'
    # self.kwargs.get('activation_key')

    def get_policy(self):
        return PolicyApplication.objects.get(user=self.request.user, id=self.kwargs.get('pk'))

    def get_queryset(self):
        return SmartDeposit.objects.filter(policy=self.get_policy().id)

    def form_valid(self, form):
        form.save()
        policy = self.get_policy()
        if policy.state == POLICY_STATUS_INIT:
            policy.submit()
            policy.submit_to_p2p_review()
            policy.save()
        elif policy.state == POLICY_STATUS_SUBMITTED:
            policy.submit_to_p2p_review()
            policy.save()
        return super(SmartDepositStubView, self).form_valid(form)