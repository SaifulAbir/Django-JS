from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import Count, QuerySet, Value, CharField
from django.db.models import Count, QuerySet
from django.db.models.query_utils import Q
from django.db.models import Count, QuerySet, Min, Max
from django.http import Http404
from datetime import date, datetime, timedelta

from django.db.models import Count
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from rest_framework.utils import json
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination

from pro.models import Professional
from resources.strings_job import *
from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill, FavouriteJob, ApplyOnline, JobCategory

from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, pagination
from .utils import favourite_job_counter, applied_job_counter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000

class JobList(generics.ListAPIView):

    queryset = Job.objects.all()
    serializer_class = JobSerializerAllField
    pagination_class = StandardResultsSetPagination



class IndustryList(generics.ListCreateAPIView):

    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class JobTypeList(generics.ListCreateAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class CurrencyList(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class Experience(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

# def Experience(self):
#     data = {
#         '1': "Fresh",
#         '2': "Less than 1 year",
#         '3': "2 Year",
#         '4': "3 Year",
#         '5':  "4 Year",
#         '6': "Above 5 Years",
#     }
#     return HttpResponse(json.dumps(data), content_type='application/json')


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

@api_view(["POST"])
def favourite_job_add(request):
    data = {}
    job_data = json.loads(request.body)

    if job_data:
        try:
            job = Job.objects.get(job_id = job_data['job_id'])
        except Job.DoesNotExist:
            job = None
        try:
            favourite_jobs = FavouriteJob.objects.filter(user = job_data['user_id'],job = job_data['job_id'])
        except FavouriteJob.DoesNotExist:
            favourite_jobs = None
        if not favourite_jobs:
            favourite_job = FavouriteJob(**job_data)
            favourite_job.save()
            favourite_job_counter(job)
            data = {
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "job": job_data['job_id'],
                        "status": 'Saved'
                    }
                }
            }
        elif favourite_jobs:
            favourite_jobs.delete()
            favourite_job_counter(job)
            data = {
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "job": job_data['job_id'],
                        "status": 'Removed'
                    }
                }
            }
    return Response(data)

class JobUpdateView(GenericAPIView, UpdateModelMixin):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CompanyPopulate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyPopulateSerializer

def load_previous_skills(request):
    previous_skills = list(Skill.objects.values_list('name', flat=True))
    return JsonResponse(previous_skills, safe=False)


@api_view(["POST"])
def trending_keyword_save(request):
    search_data = json.loads(request.body)

    if request.user_agent.is_mobile is True:
        device_name = 'Mobile'
    elif request.user_agent.is_tablet is True:
        device_name = 'Tablet'
    elif request.user_agent.is_pc is True:
        device_name = 'Computer'
    browser_name = request.user_agent.browser.family
    os_name = request.user_agent.os.family

    search_data.update([('device', device_name), ('browser', browser_name), ('operating_system', os_name)])
    print(search_data['location'])
    if search_data['location'] or search_data['keyword']:
        key_obj = TrendingKeywords(**search_data)
        key_obj.save()
        return Response(HTTP_200_OK)
    else:
        return HttpResponse('both field can not be blank')

class TrendingKeywordPopulate(generics.ListCreateAPIView):
    queryset = TrendingKeywords.objects.values('keyword').annotate(key_count = Count('keyword')).order_by('-key_count')[:6]
    serializer_class = TrendingKeywordPopulateSerializer

class PopularCategories(generics.ListCreateAPIView):
    queryset = JobCategory.objects.all().annotate(num_posts=Count('jobs')).order_by('-num_posts')[:16]
    serializer_class = PopularCategoriesSerializer

class TopSkills(generics.ListCreateAPIView):
    queryset = Skill.objects.all().annotate(skills_count=Count('skill_set')
                                            ).order_by('-skills_count')[:16]
    serializer_class = TopSkillSerializer

class PopularJobs(generics.ListCreateAPIView):
    queryset = Job.objects.all().annotate(favourite_count=Count('fav_jobs')
                                          ).order_by('-favourite_count')[:16]
    serializer_class = PopularJobSerializer





@api_view(["GET"])
def vital_stats(self):
    companies = Company.objects.all().count()
    professional = Professional.objects.all().count()
    with_deadline = Job.objects.filter(application_deadline__gte=date.today()).count()
    without_deadline = Job.objects.filter(application_deadline__isnull=True).count()
    open_job = with_deadline + without_deadline
    data ={
        'professional_count': str(professional),
        'open_job' : str(open_job),
        'resume': str(0),
        'company_count': str(companies),
    }
    return HttpResponse(json.dumps(data), content_type='application/json')






def salary_range(self):
    range_min = Job.objects.all().aggregate(Min('salary_min'))
    range_max = Job.objects.all().aggregate(Max('salary_max'))
    min_v = range_min['salary_min__min']
    max_v = range_max['salary_max__max']
    data ={
        'sr_min': str(min_v),
        'sr_max': str(max_v),
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


class SkillList(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer




@api_view(["POST"])
def apply_online_job_add(request):
    data = {}
    job_data = json.loads(request.body)


    user = User.objects.get(id = job_data['user_id'])
    j_id = job_data['job_id']

    job = Job.objects.get(job_id=j_id)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    data.update({'job': job, 'created_by': user,
                 'created_from': str(ip), 'modified_by': user,
                 'modified_from': str(ip)})
    # apply_online_job = ApplyOnline(**data)
    # print('apply_online_job', apply_online_job)
    # apply_online_job.save()
    if job_data:
        try:
            job = Job.objects.get(job_id = job_data['job_id'])
        except Job.DoesNotExist:
            job = None
        try:
            apply_online_job = ApplyOnline.objects.filter(created_by = user, job = job)
        except ApplyOnline.DoesNotExist:
            apply_online_job = None
        if not apply_online_job:
            apply_online_job = ApplyOnline(**data)

            apply_online_job.save()
            applied_job_counter(job)
            data = {
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "job": job_data['job_id'],
                        "status": 'Saved'
                    }
                }
            }

    return Response(data)


@api_view(["GET"])
def del_fav_jobs(request,identifier):
    current_user_id = request.user.id
    jobs = FavouriteJob.objects.filter(user=current_user_id)
    for job in jobs:
        if str(job.job_id)==identifier:
            job.delete()
            break

    total_bookmarked = FavouriteJob.objects.filter(user=current_user_id).count()
    data = {
        'total_bookmarked': total_bookmarked

    }
    return Response(data)