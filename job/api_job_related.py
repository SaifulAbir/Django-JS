from django.db.models import Min, Max
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from job.models import JobSource, JobCategory, JobGender, Industry, JobType, Currency, Qualification, Gender, \
    Experience, Skill, Job
from job.serializers import JobSourceSerializer, CurrencySerializer, JobTypeSerializer, IndustrySerializer, \
    QualificationSerializer, GenderSerializer, ExperienceSerializer, SkillSerializer
from resources import strings_job


class JobSourceList(generics.ListAPIView):
    queryset = JobSource.objects.filter(
        is_archived=False
    ).order_by('name')
    serializer_class = JobSourceSerializer


class JobCategoryList(generics.ListAPIView):
    queryset = JobCategory.objects.filter(
        is_archived=False
    ).order_by('name')
    serializer_class = JobSourceSerializer


class JobGenderList(generics.ListAPIView):
    queryset = JobGender.objects.filter(
        is_archived=False
    ).order_by('name')
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

@api_view(["GET"])
def get_salary_range(self):
    range_min = Job.objects.all().aggregate(Min('salary_min'))
    range_max = Job.objects.all().aggregate(Max('salary_max'))
    min_v = range_min['salary_min__min']
    max_v = range_max['salary_max__max']
    data ={
        'sr_min': str(min_v),
        'sr_max': str(max_v),
    }
    return Response(data)


class IndustryList(generics.ListAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class JobTypeList(generics.ListAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class ExperienceList(generics.ListAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class QualificationList(generics.ListAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer

class GenderList(generics.ListAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

class SkillList(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

