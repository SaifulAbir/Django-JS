from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

class CustomForbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "App token not found"

class IsAppAuthenticated(BasePermission):

    def has_permission(self, request, view):
        try:
            app_token = request.headers['api-key']
        except KeyError:
            app_token = None
        permission = bool(app_token == '96d56aceeb9049debeab628ac760aa11')
        if not permission:
            raise CustomForbidden
        else:
            return True