from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView

from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics

class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class JobList(generics.ListAPIView):

    queryset = Job.objects.all()
    serializer_class = JobSerializerAllField
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

# class CompanyPopulate(generics.ListAPIView):
#     serializer_class = CompanyPopulateSerializer
#
#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = Company.objects.all()
#         company = self.kwargs['company']
#         print(company)
#         if company is not None:
#             queryset = queryset.filter(name=company)
#             print(queryset)
#         return queryset

class CompanyPopulate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyPopulateSerializer


@api_view(["POST"])
def trending_keyword_save(request):
    search_data = json.loads(request.body)
    print(search_data)
    try:
        keyword_obj = TrendingKeywords.objects.get(keyword=search_data['keyword'])
    except TrendingKeywords.DoesNotExist:
        keyword_obj = None

    if keyword_obj is not None:
        count = keyword_obj.count +1
        keyword_obj.count = count
        keyword_obj.save()
    else:
        key_obj = TrendingKeywords(**search_data)
        key_obj.save()

    return Response(HTTP_200_OK)


