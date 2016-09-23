from django.db import models
from django.contrib.auth import get_user_model

import rest_framework_filters as filters
import django_filters

from dynamis.apps.policy.models import PolicyApplication

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


class PolicyFilter(filters.FilterSet):
    filter_overrides = {
        models.BooleanField: {
            'filter_class': django_filters.BooleanFilter,
        },
    }
    user_email = filters.CharFilter(name='user__email', lookup_type='icontains')
    user_id = filters.CharFilter(name='user__pk', lookup_type='icontains')

    class Meta:
        model = PolicyApplication
        fields = [
            'user_id',
            'user_email',
            'is_final',
            'is_signed',
        ]
