from rest_framework.permissions import BasePermission


class OwnerOnly(BasePermission):
    """Permission for owner only acions."""

    def has_object_permission(self, request, view, object_with_owner):
        return object_with_owner.owner == request.user
