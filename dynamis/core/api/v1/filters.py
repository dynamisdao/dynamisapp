from rest_framework.filters import BaseFilterBackend


class IsOwnerOrAdminFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated():
            if request.user.is_admin:
                return queryset
            return queryset.filter(user=request.user)


class IsPolicyOwnerOrAdminFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated():
            if request.user.is_admin:
                return queryset
            return queryset.filter(policy__in=request.user.policies)
