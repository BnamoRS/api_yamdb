from rest_framework.permissions import BasePermission


class IsAdminUserPermission(BasePermission):
    message = {'detail': 'Недостаточно прав доступа'}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser
        return False
