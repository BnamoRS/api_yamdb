from operator import or_
from rest_framework.permissions import BasePermission


class IsAdminUserPermission(BasePermission):
    # Фигня получилась
    message = {'detail': 'Недостаточно прав доступа'}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print(request.user.is_authenticated)
            print(request.user.role == 'AD' or request.user.is_staff or request.user.is_superuser)
            return request.user.role == 'AD' or request.user.is_staff or request.user.is_superuser
        print(request.user.is_authenticated)
        print(request.user.is_staff or request.user.is_superuser)
        return False
