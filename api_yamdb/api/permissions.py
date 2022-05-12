import imp
from rest_framework.permissions import BasePermission


class IsAdminUserPermission(BasePermission):
    message = {'detail': 'Недостаточно прав доступа'}
    
    def has_permission(self, request, view):
        return request.user.role == 'AD'
