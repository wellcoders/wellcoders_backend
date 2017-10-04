from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True

        if view.action == 'list':
            return request.user.is_authenticated and request.user.is_superuser

        return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if view.action == 'create':
            return True

        if not request.user.is_authenticated:
            return False

        if view.action in {'list', 'retrieve'} and request.user.is_superuser:
            return True

        return request.user.is_authenticated and request.user == obj

