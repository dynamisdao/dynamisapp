from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'keybase_username',
            'is_superuser',
            'is_staff',
            'is_active',
            'is_risk_assessor',
        )
