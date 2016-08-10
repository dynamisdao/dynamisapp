from django.db import models
from django.contrib.auth import get_user_model

import rest_framework_filters as filters
import django_filters


User = get_user_model()


class UserFilter(filters.FilterSet):
    # this prevents empty responses from being converted to `False` for
    # BooleanField fields.
    filter_overrides = {
        models.BooleanField: {
            'filter_class': django_filters.BooleanFilter,
        },
    }
    email = filters.CharFilter(name='email', lookup_type='icontains')

    class Meta:
        model = User
        fields = [
            'email',
            'is_staff',
            'is_superuser',
            'is_active',
            'is_risk_assessor',
        ]
