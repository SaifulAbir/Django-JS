from django.db import models
from django.db.models import Count, QuerySet
from django.http import Http404
from datetime import date

from django.db.models import Count
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView

from pro.models import Professional
from resources.strings_job import *
from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords,Skill

from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill
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

class JobObject(APIView):

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        data = JobSerializer(job).data
        data['skill']=[]
        # skills = Job_skill_detail.objects.filter(job=job)
        # skills_len = len(skills) - 1
        for skill in job.job_skills.all():
        #     if skills.index(skill) == skills_len:
            data['skill'].append(skill.name)
        #     else:
        #         data['skill'] = data['skill'] + (skill.skill.name + ', ')
        print(data)
        return Response(data)

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
    try:
        skills = job_data['skills']
        del job_data['skills']
    except KeyError:
        skills = None
    try:
        if job_data['terms_and_condition'] == ON_TXT:
            job_data['terms_and_condition'] = 1
        elif job_data['terms_and_condition'] == OFF_TXT:
            job_data['terms_and_condition'] = 0
    except KeyError:
        pass
    job_obj = Job(**job_data)
    job_obj.save()
    if skills:
        skill_list = skills.split(',')
        for skill in skill_list:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                skill_obj = None
            if skill_obj:
                job_obj.job_skills.add(skill_obj)
                # job_skills = Job_skill_detail(job=job_obj, skill=skill_obj)
                # job_skills.save()
            else:
                skill = Skill(name=skill)
                skill.save()
                job_obj.job_skills.add(skill)
                # job_skills = Job_skill_detail(job=job_obj, skill=skill)
                # job_skills.save()
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

def load_previous_skills(request):
    previous_skills = list(Skill.objects.values_list('name', flat=True))
    return JsonResponse(previous_skills, safe=False)


@api_view(["POST"])
def trending_keyword_save(request):
    search_data = json.loads(request.body)

    key_obj = TrendingKeywords(**search_data)
    key_obj.save()

    return Response(HTTP_200_OK)

class TrendingKeywordPopulate(generics.ListCreateAPIView):
    queryset = TrendingKeywords.objects.values('keyword').annotate(key_count = Count('keyword')).order_by('-key_count')[:6]
    serializer_class = TrendingKeywordPopulateSerializer

class PopularCategories(generics.ListCreateAPIView):
    queryset = Industry.objects.all().annotate(num_posts=Count('industries')).order_by('-num_posts')[:16]
    serializer_class = PopularCategoriesSerializer

class TopSkills(generics.ListCreateAPIView):
    queryset = Skill.objects.all().annotate(skills_count=Count('skill_set')
    ).order_by('-skills_count')[:16]
    serializer_class = TopSkillSerializer

class RecentJobs(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_date')[:6]
    serializer_class = JobSerializer



def vital_stats(self):
    companies = Company.objects.all().count()
    professional = Professional.objects.all().count()
    open_job = Job.objects.filter(application_deadline__gte= date.today()).count()
    data ={
        'professional_count': str(professional),
        'open_job' : str(open_job),
        'resume': str(0),
        'company_count': str(companies),
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

