from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.response import Response
from pro.models import Professional
from pro.utils import sendSignupEmail
from resources.strings_pro import *


@api_view(["POST"])
def profile_create_with_user_create(request):
    profile_data = json.loads(request.body)
    print(profile_data)
    return False
    data = {}
    if 'email' not in profile_data:
        data = {
            'status': FAILED_TXT,
            'code': 500,
            "message": EMAIL_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif 'password' not in profile_data:
        data = {
            'status': FAILED_TXT,
            'code': 500,
            "message": PASSWORD_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif 'phone' not in profile_data:
        data = {
            'status': FAILED_TXT,
            'code': 500,
            "message": MOBILE_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif User.objects.filter(email=profile_data['email']).count()>0 :
        data = {
            'status': FAILED_TXT,
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
        if profile_data['terms_and_condition_status'] == ON_TXT:
            profile_data['terms_and_condition_status']=1
        elif profile_data['terms_and_condition_status'] == OFF_TXT:
            profile_data['terms_and_condition_status'] = 0
        del profile_data['confirm_password']
        profile_obj = Professional(**profile_data)
        profile_obj.user_id=user.id
        profile_obj.save()
        #sendSignupEmail(profile_data['email'])
        data = {
            'status': 'success',
            'code': HTTP_200_OK,
            "message": 'success message here', ## will change it later
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
