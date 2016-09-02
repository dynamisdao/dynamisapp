from rest_framework import permissions


class IsAdminOrObjectOwnerPermission(permissions.BasePermission):
    message = 'Access not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated() and (request.user.is_admin or obj.user == request.user):
            return True
