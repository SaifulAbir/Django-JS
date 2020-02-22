from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.response import Response
from pro.models import Professional


@api_view(["POST"])
def profile_create_with_user_create(request):
    profile_data = json.loads(request.body)
    data = {}
    print(profile_data)
    if 'email' not in profile_data:
        data = {
            'status': 'failed',
            'code': 500,
            "message": 'Email cannot be empty',
            "result": {
                "user": {

                }
            }
        }
    elif 'password' not in profile_data:
        data = {
            'status': 'failed',
            'code': 500,
            "message": 'Password cannot be empty',
            "result": {
                "user": {

                }
            }
        }
    elif 'phone' not in profile_data:
        data = {
            'status': 'failed',
            'code': 500,
            "message": 'Mobile number cannot be empty',
            "result": {
                "user": {

                }
            }
        }
    elif User.objects.filter(email=profile_data['email']).count()>0 :
        data = {
            'status': 'failed',
            'code': 500,
            "message": 'This email already exist!!',
            "result": {
                "user": {
                    'email': profile_data['email']
                }
            }
        }
    elif profile_data['email'] and profile_data['password']:
        hash_password = make_password(profile_data['password'])
        user = User(email=profile_data['email'], password=hash_password, username=profile_data['email'])
        if user.save() :
            if profile_data['terms_and_condition_status'] == 'on':
                profile_data['terms_and_condition_status']=1
            else:
                profile_data['terms_and_condition_status'] = 0

            profile_obj = Professional(**profile_data)
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
