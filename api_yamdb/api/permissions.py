from rest_framework.permissions import SAFE_METHODS, BasePermission
# from rest_framework import permissions


class AdminOrReadOnly(BasePermission):  # переписать

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
