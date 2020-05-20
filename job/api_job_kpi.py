from pprint import pprint

from django.db import connection
from django.db.models import Count
from rest_framework import generics

from job.models import TrendingKeywords, JobCategory, Skill, Job, Company
from job.serializers import TrendingKeywordListSerializer, TopCategoriesSerializer, TopSkillSerializer, \
    TopJobSerializer, TopCompanySerializer


class TrendingKeywordList(generics.ListAPIView):
    queryset = TrendingKeywords.objects.values('keyword').annotate(key_count = Count('keyword')).order_by('-key_count')[:6]
    serializer_class = TrendingKeywordListSerializer

class TopCategoryList(generics.ListAPIView):
    queryset = JobCategory.objects.all().annotate(num_posts=Count('jobs')).order_by('-num_posts')[:16]
    serializer_class = TopCategoriesSerializer

class TopSkillList(generics.ListAPIView):
    queryset = Skill.objects.all().annotate(skills_count=Count('skill_set')
        ).filter(skill_set__status='Published', skill_set__is_archived=False
        ).order_by('-skills_count')[:16]
    serializer_class = TopSkillSerializer
    pprint(connection.queries)

class TopFavouriteList(generics.ListAPIView):
    queryset = Job.objects.all().annotate(favourite_count=Count('fav_jobs')
        ).filter(status='Published', is_archived=False
        ).order_by('-favourite_count')[:16]
    serializer_class = TopJobSerializer

class TopCompanyList(generics.ListAPIView):
    queryset = Company.objects.all().annotate(num_posts=Count('jobs')
        ).filter(jobs__status='Published', jobs__is_archived=False
        ).order_by('-num_posts')[:16]
    serializer_class = TopCompanySerializer