from rest_framework import permissions


class AccountPermission(permissions.BasePermission):
    message = 'Access not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated() and (request.user.is_admin or obj.pk == request.user.id):
            return True

    def has_permission(self, request, view):
        if request.method == 'POST' or request.user.is_authenticated():
            return True
