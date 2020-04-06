from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView
from resources.strings_job import *
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
        data['skill'] = []
        # skills = Job_skill_detail.objects.filter(job=job)
        # skills_len = len(skills) - 1

        if data['company_name'] is not None:
            ob = Company.objects.get(name=data['company_name'])
            if ob.profile_picture:
                image = ob.profile_picture
                data['profile_picture'] = '/media/' + str(image.name)
            else:
                data['profile_picture'] = '/static/images/job/company-logo-2.png'
        else:
            data['profile_picture'] = '/static/images/job/company-logo-2.png'

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
    # print(search_data)
    # try:
    #     keyword_obj = TrendingKeywords.objects.get(keyword=search_data['keyword'])
    # except TrendingKeywords.DoesNotExist:
    #     keyword_obj = None
    #
    # if keyword_obj is not None:
    #     count = keyword_obj.count + 1
    #     keyword_obj.count = count
    #
    #     if 'location' in search_data:
    #         keyword_obj.location = search_data['location']
    #     keyword_obj.save()
    # else:
    key_obj = TrendingKeywords(**search_data)
    key_obj.save()

    return Response(HTTP_200_OK)


class TrendingKeywordPopulate(generics.ListCreateAPIView):
    queryset = TrendingKeywords.objects.values('keyword').annotate(key_count=Count('keyword')).order_by('-key_count')[
               :6]
    serializer_class = TrendingKeywordPopulateSerializer
