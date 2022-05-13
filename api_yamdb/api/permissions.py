

class IsAdminUserPermission(permissioms.BasePermission):
    message = {'detail': 'Недостаточно прав доступа'}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser
        return False

from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
