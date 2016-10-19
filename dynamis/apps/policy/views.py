from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView)
from django_tables2 import SingleTableMixin
from constance import config
from rest_framework.generics import get_object_or_404

from dynamis.apps.accounts.forms import SmartDepositStubForm
from dynamis.apps.accounts.tables import SmartDepositTable
from dynamis.apps.payments.models import SmartDeposit, SMART_DEPOSIT_STATUS_INIT
from dynamis.apps.policy.models import POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED, PolicyApplication

from dynamis.utils.mixins import LoginRequired


class PolicyCreateView(DetailView):
    template_name = "policies/policy_create.html"
    context_object_name = "policy"

    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.policies.last()
        else:
            return None


class PolicyEditView(LoginRequired, DetailView):
    template_name = "policies/policy_create.html"
    context_object_name = "policy"

    def get_object(self):
        return self.request.user.policies.get(pk=self.kwargs['pk'])


class PeerReviewItemsView(LoginRequired, TemplateView):
    template_name = "policies/peer_review.html"


class SmartDepositStubView(LoginRequired, SingleTableMixin, ListView):
    template_name = "accounts/smart-deposit-stub.html"
    table_class = SmartDepositTable

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(SmartDeposit, pk=int(kwargs['pk']))
        if instance.wait_for and instance.wait_for < timezone.now():
            instance.wait_to_init()
            instance.cost_dollar = instance.cost * config.DOLLAR_ETH_EXCHANGE_RATE
            instance.save()
        return super(SmartDepositStubView, self).get(request, args, kwargs)

    @atomic
    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(SmartDeposit, pk=int(kwargs['pk']))
        form = SmartDepositStubForm(request.POST or None, instance=instance)
        if form.is_valid():
            to_return = self.form_valid(form)
        else:
            to_return = self.form_invalid(form)
        if instance.amount and instance.amount >= instance.cost:
            if instance.state == SMART_DEPOSIT_STATUS_INIT:
                instance.init_to_wait()
                instance.save()
            instance.wait_to_received()
            instance.save()
        return to_return

    def get_policy(self):
        return PolicyApplication.objects.get(user=self.request.user, id=self.kwargs.get('pk'))

    def get_queryset(self):
        return SmartDeposit.objects.filter(policy=self.get_policy().id)

    def form_valid(self, form):
        form.save()
        policy = self.get_policy()
        if policy.state == POLICY_STATUS_SUBMITTED and policy.smart_deposit.amount >= policy.smart_deposit.cost:
            policy.submit_to_p2p_review()
            policy.save()
        return HttpResponseRedirect('/policies/{}/smart-deposit/'.format(policy.pk))
