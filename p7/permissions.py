from rest_framework.permissions import BasePermission

class IsAppAuthenticated(BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        try:
            app_token = request.headers['app_token']
        except KeyError:
            app_token = None
        return bool(app_token == '123')