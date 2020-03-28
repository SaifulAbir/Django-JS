from rest_framework.decorators import api_view, permission_classes
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core.paginator import Paginator

from pro.models import Professional
from registration.models import Registration
from registration.serializers import RegistrationSerializer
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
from exam.serializers import ExamSerializer, FeaturedExamSerializer, EnrolleedExamSerializer
from exam.models import Exam
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from rest_framework import generics
from resources.strings_registration import *


@api_view(["GET"])
def dashboard(request, user_id):

    ## Chick professional id exist on db or not
    try:
        professional_id= User.objects.get(id=user_id)

        ##2. Get enrolled exam from registration table
        ## Get enrolled exam id form registration table based on professional id
        try:
            enrolled_exam_list =list(Registration.objects.filter(professional_id=user_id, status=REGISTRATION_STATUS_ZERO).values_list('exam_id', flat=True))
            enrolled_exam_list_exam_id = enrolled_exam_list

            ## Get Exam Info from Exam Table based on exam id from registration table
            try:
                enrolled_exam_list= Exam.objects.filter(pk__in=enrolled_exam_list).order_by('-id')
                enrolled_exam_list = EnrolleedExamSerializer(enrolled_exam_list, many=True)
            except Exam.DoesNotExist:
                enrolled_exam_list = []
        except Registration.DoesNotExist:
            enrolled_exam_list_exam_id = []
            enrolled_exam_list = []

        ##1. Feature exam model query ##
        try:
            featured_exam_list =Exam.objects.exclude(id__in=enrolled_exam_list_exam_id).exclude(is_featured='0').order_by('-id')
            featured_exam_list = FeaturedExamSerializer(featured_exam_list, many=True)
        except Exam.DoesNotExist:
            featured_exam_list = []

        ##3. Get recent exam result form registration table based on status

        try:
            recent_exam_list =list(Registration.objects.filter(professional_id=user_id, status=REGISTRATION_STATUS_ONE).order_by('-id'))
            recent_exam_list= RegistrationSerializer(recent_exam_list, many=True)


            ## Get Exam Info from Exam Table based on exam id from registration table
            # try:
            #     recent_exam_list= Exam.objects.filter(pk__in=recent_exam_list).order_by('-id')
            #     recent_exam_list = ExamSerializer(recent_exam_list, many=True)
            # except Exam.DoesNotExist:
            #     recent_exam_list = []
        except Registration.DoesNotExist:
            recent_exam_list = []

        data= {
            'status': 'success',
            'code': HTTP_200_OK,
            "data": {
                "user": {
                    "name": professional_id.email,
                    'id': user_id,
                    'profile_pic_url': "https://icon-library.net/images/default-user-icon/default-user-icon-4.jpg",
                    'email': professional_id.email
                },
                "featured_exam": featured_exam_list.data,
                "enrolled_exam": enrolled_exam_list.data,
                "recent_exam": recent_exam_list.data,
                "exam_chart": {
                    'percentage_of_pass': 80,
                    'percentage_of_fail': 20
                }
            }
        }
    except User.DoesNotExist:
        data = {
            'status': 'failed',
            'code': HTTP_404_NOT_FOUND,
            "data": ''
        }


    return Response(data, HTTP_200_OK)


@api_view(["GET"])
def professional_info(request, user_id):
    try:
        user= User.objects.get(id=user_id)
        try:
            professional = Professional.objects.get(user_id=user.id)
            data = {
                'status': 'success',
                'code': HTTP_200_OK,
                "data": {
                    "user": {
                        "name": professional.full_name,
                        "mobile_number": professional.phone,
                        'id': user_id,
                        'profile_pic_url': "https://icon-library.net/images/default-user-icon/default-user-icon-4.jpg",
                        'email': professional.email,
                        'address': professional.address,
                        'about': "Entrepreneur and businessman Bill Gates and his business partner Paul Allen founded and built the world's largest software business, Microsoft, through technological innovation, keen business strategy and aggressive business tactics. In the process, Gates became one of the richest men in the world.",
                        'city': 'Dhaka',
                    }
                }
            }
        except Professional.DoesNotExist:
            data = {
                'status': 'failed',
                'code': HTTP_404_NOT_FOUND,
                "data": ''
            }
        return Response(data, HTTP_200_OK)
    except Professional.DoesNotExist:
        data = {
            'status': 'failed',
            'code': HTTP_404_NOT_FOUND,
            "data": ''
        }
        return Response(data, HTTP_200_OK)

    try:
        professional= Professional.objects.get(user_id=user.id)
        data= {
            'status': 'success',
            'code': HTTP_200_OK,
            "data": {
                "user": {
                    "name": professional.full_name,
                    "mobile_number": professional.phone,
                    'id': user_id,
                    'profile_pic_url': "https://icon-library.net/images/default-user-icon/default-user-icon-4.jpg",
                    'email': professional.email,
                    'address': professional.address,
                    'about': "Entrepreneur and businessman Bill Gates and his business partner Paul Allen founded and built the world's largest software business, Microsoft, through technological innovation, keen business strategy and aggressive business tactics. In the process, Gates became one of the richest men in the world.",
                    'city': 'Dhaka',
                }
            }
        }
    except Professional.DoesNotExist:
        data = {
            'status': 'failed',
            'code': HTTP_404_NOT_FOUND,
            "data": ''
        }


    return Response(data, HTTP_200_OK)

# class RecentJobs(generics.ListCreateAPIView):
#     queryset = Industry.objects.all().annotate(num_posts=Count('industries')).order_by('-num_posts')[:16]
#     serializer_class = PopularCategoriesSerializer
