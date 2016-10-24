from django import forms

from dynamis.apps.payments.models import SmartDeposit, FillEthOperation
from dynamis.apps.policy.models import RiskAssessmentTask


class SmartDepositStubForm(forms.ModelForm):
    class Meta:
        model = SmartDeposit
        fields = (
            'amount_dollar',
            'policy'
        )


class FillEthOperationForm(forms.ModelForm):
    class Meta:
        model = FillEthOperation
        fields = (
            'eth_account',
            'amount',
        )


class RiskAssessmentTaskForm(forms.ModelForm):
    class Meta:
        model = RiskAssessmentTask
        fields = (
            'policy',
            'bet1',
            'bet2',
            'question1',
            'question2'
        )
