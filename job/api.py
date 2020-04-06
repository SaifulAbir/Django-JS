from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import Count, QuerySet, Value, CharField
from django.db.models import Count, QuerySet
from django.db.models.query_utils import Q
from django.db.models import Count, QuerySet, Min, Max
from django.http import Http404
from datetime import date

from django.db.models import Count
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination

from pro.models import Professional
from resources.strings_job import *
from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill, FavouriteJob

from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, pagination


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
    permission_classes = ([IsAuthenticated])
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        try:
            favourite_job = FavouriteJob.objects.get(job=job, user=self.request.user)
        except FavouriteJob.DoesNotExist:
            favourite_job = None
        if favourite_job is not None:
            job.status = YES_TXT
        else:
            job.status = NO_TXT
        data = JobSerializer(job).data
        data['skill']=[]
        # skills = Job_skill_detail.objects.filter(job=job)
        # skills_len = len(skills) - 1
        for skill in job.job_skills.all():
            #     if skills.index(skill) == skills_len:
            data['skill'].append(skill.name)
        #     else:
        #         data['skill'] = data['skill'] + (skill.skill.name + ', ')
        return Response(data)

class IndustryList(generics.ListCreateAPIView):

    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class JobTypeList(generics.ListCreateAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

@api_view(["GET"])
def job_list(request):
    try:
        query = request.GET.get('q')
        sorting = request.GET.get('sort')

        if sorting == 'descending':
            job_list = Job.objects.all().order_by('-created_date')
            print(job_list)
        else:
            job_list = Job.objects.all()


        if query:
             job_list = job_list.filter(
                 Q(title__icontains=query)
             ).distinct()

        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 2)

        default_number_of_row = 2
        paginator = Paginator(job_list, page_size)

        try:
            job_list = paginator.page(page)
        except PageNotAnInteger:
            job_list = paginator.page(1)
        except EmptyPage:
            job_list = paginator.page(1)

        number_of_row_total = paginator.count
        number_of_pages = paginator.num_pages
        check_next_available_or_not = paginator.page(page).has_next()
        job_list = JobSerializer(job_list, many=True)

    except Job.DoesNotExist:
         job_list = []


    data = {
        'status': 'success',
        'count': number_of_row_total,
        'number_of_pages': number_of_pages,
        'next_pages': check_next_available_or_not,
        'code': HTTP_200_OK,
        "results":  job_list.data,
    }
    return Response(data, HTTP_200_OK)

class CurrencyList(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


def Experience(self):
    data = {
        '1': "Fresh",
        '2': "Less than 1 year",
        '3': "2 Year",
        '4': "3 Year",
        '5':  "4 Year",
        '6': "Above 5 Years",
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


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
            favourite_jobs = FavouriteJob.objects.filter(user = job_data['user_id'],job = job_data['job_id'])
        except FavouriteJob.DoesNotExist:
            favourite_jobs = None
        if not favourite_jobs:
            favourite_job = FavouriteJob(**job_data)
            favourite_job.save()
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

class PopularJobs(generics.ListCreateAPIView):
    queryset = Job.objects.all().annotate(favourite_count=Count('fav_jobs')
    ).order_by('-favourite_count')[:16]
    serializer_class = PopularJobSerializer

@api_view(["GET"])
def recent_jobs(request):
    queryset = Job.objects.all().annotate(status=Value('', output_field=CharField())).order_by('-created_date')[:6]
    data = []
    for job in queryset:
        try:
            favourite_job = FavouriteJob.objects.get(job=job, user=request.user)
        except FavouriteJob.DoesNotExist:
            favourite_job = None
        if favourite_job is not None:
            job.status = YES_TXT
        else:
            job.status = NO_TXT
        if job.company_name:
            if job.company_name.profile_picture:
                job.profile_picture = '/media/' + str(job.company_name.profile_picture)
            else:
                job.profile_picture = '/static/images/job/company-logo-2.png'
        else:
            job.profile_picture = '/static/images/job/company-logo-2.png'
        data.append({'job_id':job.job_id, 'title':job.title, 'job_location':job.job_location, 'created_date':job.created_date, 'status':job.status, 'profile_picture':job.profile_picture, 'employment_status':str(job.employment_status), 'company_name':str(job.company_name)})
    return JsonResponse(list(data), safe=False)

@api_view(["GET"])
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

@api_view(["GET"])
def similar_jobs(request,industry):

    queryset = Job.objects.filter(industry=industry).order_by('-created_date')[:5]
    data = []
    for job in queryset:
        try:
            favourite_job = FavouriteJob.objects.get(job=job, user=request.user)
        except FavouriteJob.DoesNotExist:
            favourite_job = None
        if favourite_job is not None:
            job.status = 'Yes'
        else:
            job.status = 'No'
        if job.company_name:
            if job.company_name.profile_picture:
                job.profile_picture = '/media/' + str(job.company_name.profile_picture)
            else:
                job.profile_picture = '/static/images/job/company-logo-2.png'
        else:
            job.profile_picture = '/static/images/job/company-logo-2.png'
        data.append({'job_id': job.job_id, 'title': job.title, 'job_location': job.job_location,
                     'created_date': job.created_date, 'status': job.status, 'profile_picture': job.profile_picture,
                     'employment_status': str(job.employment_status), 'company_name': str(job.company_name)})
    return JsonResponse(list(data), safe=False)


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
