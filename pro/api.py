from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.utils import json
from rest_framework.response import Response
from pro.models import Professional
from resources.strings_pro import *
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from resources.strings_pro import *


@api_view(["POST"])
def profile_create_with_user_create(request):
    profile_data = json.loads(request.body)
    data = {}
    if 'email' not in profile_data:
        data = {
            'status': 'failed',
            'code': 500,
            "message": EMAIL_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif 'password' not in profile_data:
        data = {
            'status': 'failed',
            'code': 500,
            "message": PASSWORD_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif 'phone' not in profile_data:
        data = {
            'status': 'failed',
            'code': 500,
            "message": MOBILE_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif User.objects.filter(email=profile_data['email']).count()>0 :
        data = {
            'status': 'failed',
            'code': 500,
            "message": EMAIL_EXIST_ERROR_MSG,
            "result": {
                "user": {
                    'email': profile_data['email']
                }
            }
        }
    elif profile_data['email'] and profile_data['password']:
        hash_password = make_password(profile_data['password'])
        user = User(email=profile_data['email'], password=hash_password, username=profile_data['email'], is_active=0)
        user.save()
        if profile_data['terms_and_condition_status'] == 'on':
            profile_data['terms_and_condition_status']=1
        elif profile_data['terms_and_condition_status'] == 'off':
            profile_data['terms_and_condition_status'] = 0
        del profile_data['confirm password']
        profile_obj = Professional(**profile_data)
        profile_obj.user_id=user.id
        profile_obj.save()
        data = {
            'status': 'success',
            'code': HTTP_200_OK,
            "message": 'ok',
            "result": {
                "user": {
                    "email": profile_data['password'],
                }
            }
        }
    return Response(data)

@api_view(["POST"])
def profile_create(request):
    profile_data = json.loads(request.body)
    profile_data['password'] = make_password(profile_data['password'])
    profile_obj = Professional(**profile_data)
    profile_obj.save()
    return Response(HTTP_200_OK)

@api_view(["POST"])
def login(request):
    login_data = json.loads(request.body)
    if login_data["email"] is None or login_data["password"] is None:
        return Response({'error': LOGIN_CREDENTIAL_BLANK_ERROR},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=login_data["email"], password=login_data["password"])
    if not user:
        return Response({'error': LOGIN_CREDENTIAL_ERROR_MSG},
                        status=HTTP_404_NOT_FOUND)
    elif user.is_active == False:
        return Response({'error': LOGIN_CREDENTIAL_ERROR_MSG},
                        status=HTTP_404_NOT_FOUND)
    # token, _ = Token.objects.get_or_create(user=user)
    return Response(status=HTTP_200_OK)
