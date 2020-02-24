from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.utils import json
from rest_framework.response import Response
from rest_framework.views import APIView

from pro.models import Professional
from pro.serializers import ProfessionalSerializer
from resources.strings_pro import *
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
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
    return Response(HTTP_200_OK)

class ProfessionalDetail(APIView):
    def get(self, request, pk):
        profile = get_object_or_404(Professional, pk=pk)
        data = ProfessionalSerializer(profile).data
        return Response(data)

class ProfessionalUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Professional.objects.get(pk=pk)
        except Professional.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfessionalSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
