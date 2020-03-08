from rest_framework.permissions import BasePermission


class IsAppAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.header.app_token == '123')