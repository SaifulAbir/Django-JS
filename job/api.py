from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class JobListViaPackage(generics.ListAPIView):
    serializer_class = JobSerializerAllField
    queryset = Job.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('title', 'salary_min')
    ordering_fields = ('title', 'salary_min')
    ordering = ('title')
    search_fields = ('title', 'salary_min')
    pagination_class = StandardResultsSetPagination

class JobList(generics.ListAPIView):
    serializer_class = JobSerializerAllField
    queryset = Job.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('title', 'salary_min')
    ordering_fields = ('title', 'salary_min')
    ordering = ('title')
    search_fields = ('title', 'salary_min')
    pagination_class = StandardResultsSetPagination

class JobObject(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        job = self.kwargs['pk']
        if job is not None:
            queryset = queryset.filter(job_id=job)
        return queryset

class IndustryList(generics.ListCreateAPIView):

    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class JobTypeList(generics.ListCreateAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class CurrencyList(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class ExperienceList(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class QualificationList(generics.ListCreateAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer

class GenderList(generics.ListCreateAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

@api_view(["POST"])
def job_create(request):
    job_data = json.loads(request.body)
    job_obj = Job(**job_data)
    job_obj.save()
    return Response(HTTP_200_OK)

class JobUpdateView(GenericAPIView, UpdateModelMixin):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class CompanyPopulate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyPopulateSerializer

@api_view(["GET"])
def featured_examlist(request):
    check_next_available_or_not = ''
    try:
        featured_exam_list = Job.objects.all()
        query = request.GET.get('q')

        if query:
            featured_exam_list = featured_exam_list.filter(
                Q(title__icontains=query)
            ).distinct().order_by('-id')

        page = request.GET.get('page', 1)
        if not page:
            page = 1

        default_number_of_row = PageNumberPagination.page_size

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

        a = JobSerializerAllField(featured_exam_list, many=True)
    except Job.DoesNotExist:
        a = []
    data = {
        'status': 'success',
        'next_pages': check_next_available_or_not,
        'code': HTTP_200_OK,
        "data": {
            "b": a.data,
        }
    }
    return Response(data, HTTP_200_OK)
