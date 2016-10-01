from django import forms

from dynamis.apps.payments.models import SmartDeposit, FillEthOperation


class SmartDepositStubForm(forms.ModelForm):
    class Meta:
        model = SmartDeposit
        fields = (
            'is_confirmed',
            'amount',
            'policy'
        )


class FillEthOperationForm(forms.ModelForm):
    class Meta:
        model = FillEthOperation
        fields = (
            'eth_account',
            'amount',
        )
