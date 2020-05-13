from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from job.models import JobSource, JobCategory, JobGender
from job.serializers import JobSourceSerializer
from resources import strings_job


class JobSourceList(generics.ListAPIView):
    queryset = JobSource.objects.all()
    serializer_class = JobSourceSerializer


class JobCategoryList(generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobSourceSerializer


class JobGenderList(generics.ListAPIView):
    queryset = JobGender.objects.all()
    serializer_class = JobSourceSerializer


@api_view(["GET"])
def get_job_site_list(request):
    return Response(strings_job.JOB_SITES)

@api_view(["GET"])
def get_job_nature_list(request):
    return Response(strings_job.JOB_NATURES)

@api_view(["GET"])
def get_job_type_list(request):
    return Response(strings_job.JOB_TYPES)

@api_view(["GET"])
def get_job_status_list(request):
    return Response(strings_job.JOB_STATUSES)

@api_view(["GET"])
def get_job_creator_type_list(request):
    return Response(strings_job.JOB_CREATOR_TYPES)

