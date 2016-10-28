import json

import requests
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
from rest_framework.reverse import reverse

from dynamis.apps.accounts.forms import SmartDepositStubForm
from dynamis.apps.accounts.tables import SmartDepositTable
from dynamis.apps.payments.business_logic import check_transfers_change_model_states
from dynamis.apps.payments.models import SmartDeposit, WAIT_FOR_TX_STATUS_INIT, WAIT_FOR_TX_STATUS_WAITING
from dynamis.apps.policy.models import POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED, PolicyApplication
from dynamis.utils.math import approximately_equal

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


class SmartDepositView(LoginRequired, SingleTableMixin, ListView):
    template_name = "accounts/smart-deposit.html"
    table_class = SmartDepositTable
    object_list = SmartDeposit.objects.all()

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(SmartDeposit, pk=int(kwargs['pk']))
        check_transfers_change_model_states(instance)
        return super(SmartDepositView, self).get(request, args, kwargs)

    def get_queryset(self):
        return SmartDeposit.objects.filter(policy=self.get_policy().id)

    def get_policy(self):
        return PolicyApplication.objects.get(user=self.request.user, id=self.kwargs.get('pk'))


class SmartDepositStubView(LoginRequired, SingleTableMixin, ListView):
    template_name = "accounts/smart-deposit-stub.html"
    table_class = SmartDepositTable
    object_list = SmartDeposit.objects.all()

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(SmartDeposit, pk=int(kwargs['pk']))
        if instance.state == WAIT_FOR_TX_STATUS_INIT:
            instance.init_to_wait()
            instance.save()
        if not instance.exchange_rate_at_invoice_time:
            instance.exchange_rate_at_invoice_time = config.DOLLAR_ETH_EXCHANGE_RATE
            instance.save()
        if instance.state == WAIT_FOR_TX_STATUS_WAITING and instance.wait_for and instance.wait_for < timezone.now():
            instance.wait_to_init()
            instance.init_to_wait()
            instance.cost = instance.cost_dollar / config.DOLLAR_ETH_EXCHANGE_RATE
            instance.save()
        check_transfers_change_model_states(instance)
        return super(SmartDepositStubView, self).get(request, args, kwargs)

    def get_queryset(self):
        return SmartDeposit.objects.filter(policy=self.get_policy().id)

    def get_policy(self):
        return PolicyApplication.objects.get(user=self.request.user, id=self.kwargs.get('pk'))

    @atomic
    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(SmartDeposit, pk=int(kwargs['pk']))
        form = SmartDepositStubForm(request.POST or None, instance=instance)
        if form.is_valid():
            to_return = self.form_valid(form)
        else:
            to_return = self.form_invalid(form)
        if instance.amount and approximately_equal(instance.amount, instance.cost, config.TX_VALUE_DISPERSION):
            if instance.state == WAIT_FOR_TX_STATUS_INIT:
                instance.init_to_wait()
                instance.save()
            instance.wait_to_received()
            instance.save()
        return to_return

    @atomic
    def form_valid(self, form):
        form.save()
        policy = self.get_policy()
        amount = policy.smart_deposit.amount_dollar / config.DOLLAR_ETH_EXCHANGE_RATE
        if policy.state == POLICY_STATUS_SUBMITTED and approximately_equal(amount,
                                                                           policy.smart_deposit.cost,
                                                                           config.TX_VALUE_DISPERSION):
            policy.smart_deposit.amount = amount
            policy.smart_deposit.save()
            policy.smart_deposit.wait_to_received()
            policy.smart_deposit.save()
        return HttpResponseRedirect('/policies/{}/smart-deposit-fake/'.format(policy.pk))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
