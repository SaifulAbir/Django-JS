from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission
from django.utils.deprecation import MiddlewareMixin

class ApiKeyForbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Invalid API key"

class IsAppAuthenticated(BasePermission):

    def has_permission(self, request, view):
        try:
            app_token = request.headers['api-key']
        except KeyError:
            app_token = None
        permission = bool(app_token == '96d56aceeb9049debeab628ac760aa11')
        if not permission:
            raise ApiKeyForbidden
        else:
            return True