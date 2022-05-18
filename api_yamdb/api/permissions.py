from rest_framework import permissions


class IsAdminUserPermission(permissions.BasePermission):
    message = {'detail': 'Недостаточно прав доступа'}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_staff
                or request.user.is_superuser
            )
        return False


class IsAuthorUserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(type(obj.author))
        print(type(request.user))
        print(obj.author is request.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsModerUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'moderator'
        return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class CommentRewiewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user.is_staff
                or request.user.is_superuser
            )
        return False
