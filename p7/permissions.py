from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

class CustomForbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "App token not found"

class IsAppAuthenticated(BasePermission):

    def has_permission(self, request, view):
        try:
            app_token = request.headers['app_token']
        except KeyError:
            app_token = None
        permission = bool(app_token == '123')
        if not permission:
            raise CustomForbidden
        else:
            return True