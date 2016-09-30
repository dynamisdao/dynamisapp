from django import forms

from dynamis.apps.payments.models import SmartDeposit


class SmartDepositStubForm(forms.ModelForm):
    class Meta:
        model = SmartDeposit
        fields = (
            'is_confirmed',
            'amount',
            'user'
        )
