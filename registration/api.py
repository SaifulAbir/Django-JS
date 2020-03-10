from django.conf.urls import url
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core.paginator import Paginator
from registration.models import Registration
from registration.serializers import RegistrationSerializer
from registration.utils import checkDuplicateRegistration
from resources.strings import *
from django.core import serializers
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)
from rest_framework import pagination
from django.db.models import Q
from exam.serializers import *
from exam.models import *
from rest_framework.filters import SearchFilter, OrderingFilter
from resources.strings_registration import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(["POST"])
def exam_enroll(request):
    received_json_data = json.loads(request.body)
    exam_id = received_json_data["exam_id"]
    professional_id = received_json_data["professional_id"]
    status= True
    ERROR_MESSAGE= EXAM_ENROLLED_FAILED_MESSAGE
    try:
        Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        status=False

    try:
        User.objects.get(id=professional_id)
    except User.DoesNotExist:
        status= False

    status =checkDuplicateRegistration(professional_id,exam_id)



    if status:
        reg= Registration.objects.create(professional_id=professional_id, exam_id=exam_id, status=REGISTRATION_STATUS_ZERO)
        ERROR_MESSAGE = ''
    else:
        ERROR_MESSAGE = DUPLICATE_ENTRY_NOT_ALLOWED


    if status:
        data= {
            'status': SUCCESS,
            'code': HTTP_200_OK,
            "message": EXAM_ENROLLED_SUCCESFULL_MESSAGE,
            "result": {
                "reg_id": reg.id,

            }
        }
    else:
        data = {
            'status': FAILED,
            'code': HTTP_401_UNAUTHORIZED,
            "message": ERROR_MESSAGE,
            "result": {
                "user": {
                    "reg_id": ''
                }
            }
        }

    return Response(data)