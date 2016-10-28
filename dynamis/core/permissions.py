from rest_framework import permissions


class IsAdminOrObjectOwnerPermission(permissions.BasePermission):
    message = 'Access not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated() and (request.user.is_admin or obj.user == request.user):
            return True


class IsAdminOrPolicyOwnerPermission(permissions.BasePermission):
    message = 'Access not allowed.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated() or not request.user.policies.exists():
            return False
        if request.user.is_admin or obj.policy.user == request.user:
            return True


class IsRiskAssessorPermission(permissions.BasePermission):
    message = 'Access not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated() and request.user.is_risk_assessor:
            return True
