from django.conf.urls import url
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core.paginator import Paginator
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
from exam.serializers import *
from exam.models import *
from rest_framework.filters import SearchFilter, OrderingFilter
from resources.strings_registration import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(["GET"])
def enrolled_examlist(request, user_id):
    ##2. Get enrolled exam from registration table
    ## Get enrolled exam id form registration table based on examinee id
    try:
        enrolled_exam_list = list(
            Registration.objects.filter(professional_id=user_id, status=REGISTRATION_STATUS_ZERO).values_list('exam_id',
                                                                                                           flat=True).order_by('-id'))
        ## Get Exam Info from Exam Table based on exam id from registration table
        try:
            enrolled_exam_list = Exam.objects.filter(pk__in=enrolled_exam_list).order_by('-id')

            query = request.GET.get('q')

            if query:
                enrolled_exam_list = enrolled_exam_list.filter(
                    Q(exam_name__icontains=query)
                ).distinct().order_by('-id')

            page = request.GET.get('page', 1)
            if not page:
                page = 1

            default_number_of_row = pagination.PageNumberPagination.page_size
            paginator = Paginator(enrolled_exam_list, default_number_of_row)

            try:
                enrolled_exam_list = paginator.page(page)
            except PageNotAnInteger:
                enrolled_exam_list = paginator.page(1)
            except EmptyPage:
                enrolled_exam_list = paginator.page(1)

            number_of_row_total = paginator.count
            number_of_pages = paginator.num_pages
            check_next_available_or_not = paginator.page(page).has_next()

            enrolled_exam_list = EnrolleedExamSerializer(enrolled_exam_list, many=True)
        except Exam.DoesNotExist:
            enrolled_exam_list = []
    except Registration.DoesNotExist:
        enrolled_exam_list = []

    data = {
        'status': 'success',
        'next_pages': check_next_available_or_not,
        'code': HTTP_200_OK,
        "data": {
            "enrolled_exam": enrolled_exam_list.data,
        }
    }
    return Response(data, HTTP_200_OK)

@api_view(["GET"])
def featured_examlist(request, user_id):
    try:
        enrolled_exam_list = list(Registration.objects.filter(professional_id=user_id, status=REGISTRATION_STATUS_ZERO).values_list('exam_id', flat=True).order_by('-id'))
        enrolled_exam_list_exam_id = enrolled_exam_list

    except Registration.DoesNotExist:
        data = {
            'status': 'success',
            'next_pages': 'False',
            'code': HTTP_200_OK,
            "data": {
                "featured_exam_list": [],
            }
        }
        return Response(data, HTTP_200_OK)

    try:
        featured_exam_list = Exam.objects.exclude(id__in=enrolled_exam_list_exam_id).exclude(is_featured='0').order_by('-id')
        query= request.GET.get('q')

        if query:
            featured_exam_list= featured_exam_list.filter(
                Q(exam_name__icontains=query)
            ).distinct().order_by('-id')

        page = request.GET.get('page', 1)
        if not page:
            page = 1

        default_number_of_row = pagination.PageNumberPagination.page_size
        paginator = Paginator(featured_exam_list, default_number_of_row)

        try:
            featured_exam_list = paginator.page(page)
        except PageNotAnInteger:
            featured_exam_list = paginator.page(1)
        except EmptyPage:
            featured_exam_list = paginator.page(1)

        number_of_row_total = paginator.count
        number_of_pages = paginator.num_pages
        check_next_available_or_not = paginator.page(page).has_next()


        featured_exam_list = FeaturedExamSerializer(featured_exam_list, many=True)
    except Exam.DoesNotExist:
        featured_exam_list = []
    data = {
        'status': 'success',
        'next_pages':check_next_available_or_not,
        'code': HTTP_200_OK,
        "data": {
            "featured_exam_list": featured_exam_list.data,
        }
    }
    return Response(data, HTTP_200_OK)

@api_view(["GET"])
def recent_examlist(request, user_id):
    ## Chick examinee id exist on db or not
    try:
        recent_exam_list = Registration.objects.filter(professional_id=user_id, status=REGISTRATION_STATUS_ONE).order_by('-id')

        query = request.GET.get('q')

        if query:
            recent_exam_list = recent_exam_list.filter(
                Q(exam__exam_name__icontains=query)
            ).distinct().order_by('-id')

        ## Pagination Start
        page = request.GET.get('page', 1)
        if not page:
            page = 1

        default_number_of_row = pagination.PageNumberPagination.page_size
        paginator = Paginator(recent_exam_list, default_number_of_row)

        try:
            recent_exam_list = paginator.page(page)
        except PageNotAnInteger:
            recent_exam_list = paginator.page(1)
        except EmptyPage:
            recent_exam_list = paginator.page(1)

        number_of_row_total = paginator.count
        number_of_pages = paginator.num_pages
        check_next_available_or_not = paginator.page(page).has_next()
    ## Pagination End

        recent_exam_list = RegistrationSerializer(recent_exam_list, many=True)

    except Registration.DoesNotExist:
        recent_exam_list = []

    data = {
        'status': 'success',
        'next_pages': check_next_available_or_not,
        'code': HTTP_200_OK,
        "data": {
            "recent_exam_list": recent_exam_list.data,
        }
    }
    return Response(data, HTTP_200_OK)

@api_view(["GET"])
def exam_instruction(request, exam_id):
    ## Chick examinee id exist on db or not
    try:
        exam= Exam.objects.get(id=exam_id)
        exam = FeaturedExamSerializer(exam)
        data= {
            'status': 'success',
            'code': HTTP_200_OK,
            "data": {
                "exam": exam.data,
            }
        }
    except Exam.DoesNotExist:
        data = {
            'status': 'failed',
            'code': HTTP_404_NOT_FOUND,
            "data": ''
        }
    return Response(data, HTTP_200_OK)


@api_view(["GET"])
def recent_examlist(request, user_id):
    ## Chick examinee id exist on db or not
    try:
        recent_exam_list = Registration.objects.filter(professional_id=user_id, status=REGISTRATION_STATUS_ONE).order_by('-id')

        query = request.GET.get('q')

        if query:
            recent_exam_list = recent_exam_list.filter(
                Q(exam__exam_name__icontains=query)
            ).distinct().order_by('-id')

        ## Pagination Start
        page = request.GET.get('page', 1)
        if not page:
            page = 1

        default_number_of_row = pagination.PageNumberPagination.page_size
        paginator = Paginator(recent_exam_list, default_number_of_row)

        try:
            recent_exam_list = paginator.page(page)
        except PageNotAnInteger:
            recent_exam_list = paginator.page(1)
        except EmptyPage:
            recent_exam_list = paginator.page(1)

        number_of_row_total = paginator.count
        number_of_pages = paginator.num_pages
        check_next_available_or_not = paginator.page(page).has_next()
    ## Pagination End

        recent_exam_list = RegistrationSerializer(recent_exam_list, many=True)

    except Registration.DoesNotExist:
        recent_exam_list = []

    data = {
        'status': 'success',
        'next_pages': check_next_available_or_not,
        'code': HTTP_200_OK,
        "data": {
            "recent_exam_list": recent_exam_list.data,
        }
    }
    return Response(data, HTTP_200_OK)