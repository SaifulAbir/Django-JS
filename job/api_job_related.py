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
    data = [{'id': item[0], 'text': item[1]} for item in strings_job.JOB_SITES]
    return Response(data)

@api_view(["GET"])
def get_job_nature_list(request):
    data = [{'id': item[0], 'text': item[1]} for item in strings_job.JOB_NATURES]
    return Response(data)

@api_view(["GET"])
def get_job_type_list(request):
    data = [{'id': item[0], 'text': item[1]} for item in strings_job.JOB_TYPES]
    return Response(data)

@api_view(["GET"])
def get_job_status_list(request):
    data = [{'id': item[0],'text': item[1]} for item in strings_job.JOB_STATUSES]
    return Response(data)

@api_view(["GET"])
def get_job_creator_type_list(request):
    data = [{'id': item[0],'text': item[1]} for item in strings_job.JOB_CREATOR_TYPES]
    return Response(data)

