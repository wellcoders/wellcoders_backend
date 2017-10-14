from rest_framework.permissions import BasePermission


class CommentPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action in {"list", "retrieve"}:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if view.action == "retrieve":
            return True

        if view.action == "create":
            return request.user.is_authenticated

        if view.action in {"update", "partial_update"}:
            return request.user.is_authenticated and request.user.pk == obj.owner.pk

        return request.user.is_authenticated and request.user == obj.owner

