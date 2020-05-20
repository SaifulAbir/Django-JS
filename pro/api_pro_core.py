

from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from django.contrib.auth.hashers import make_password
from . import serializers
from rest_framework.permissions import IsAuthenticated

from .utils import *


@api_view(["POST"])
def change_password(request):
    received_json_data = json.loads(request.body)
    user = received_json_data["user_id"]
    old_password = received_json_data["old_password"]
    new_password = received_json_data["new_password"]

    try:
        user_obj = User.objects.get(id=user)
    except User.DoesNotExist:
        data = {
            'status': 'failed',
            'code': HTTP_401_UNAUTHORIZED,
            "message": USER_ID_NOT_EXIST,
            "result": ''
        }
        return Response(data, HTTP_401_UNAUTHORIZED)
    status = check_password(old_password, user_obj.password)

    if not status :
        data = {
            'status': 'failed',
            'code': HTTP_401_UNAUTHORIZED,
            "message": WRONG_OLD_PASSWORD_MSG,
            "result": ''
        }
        return Response(data, HTTP_401_UNAUTHORIZED)
    else:
        new_password = make_password(new_password)
        user_obj.password = new_password
        user_obj.save()

        data = {
            'status': 'success',
            'code': HTTP_200_OK,
            "message": PASSWORD_CHANGED_SUCCESS_MSG,
            "result": {
                "user": {
                    "username": user_obj.username,
                    'user_id': user_obj.id
                }
            }
        }
    return Response(data, HTTP_200_OK)


