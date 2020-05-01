from rest_framework import serializers
from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill, ApplyOnline
from rest_framework.validators import *


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, label='company_name')
    # contact_no = serializers.CharField(required=True, max_length=11)
    email = serializers.CharField(max_length=30, validators=[UniqueValidator(queryset=Company.objects.all())])

    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {'client': {'required': False}}


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['name']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name']

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['name']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['name']

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['name']

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['name']



class JobSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    is_applied = serializers.CharField(read_only=True)
    class Meta:
        model = Job
        fields = ('status','is_applied', 'job_id','title','industry','employment_status','job_location','experience'
            ,'salary_min' ,'salary_max','qualification','gender' ,'currency' ,'vacancy' ,'application_deadline'
            ,'descriptions' ,'responsibilities','education','salary' ,'other_benefits','company_name','division'
            ,'district','zipcode' ,'company_location' ,'company_profile','latitude','longitude','raw_content','web_address','terms_and_condition'
            ,'created_date','job_skills', 'slug')

class RecentJobSerializer(serializers.ModelSerializer):

    status = serializers.CharField()
    # profile_picture = serializers.CharField()

    class Meta:
        model = Job
        fields = ['job_location', 'job_id', 'company_name', 'employment_status', 'title', 'created_date', 'status']

class JobSerializerAllField(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class CompanyPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'web_address', 'company_profile']

class TrendingKeywordPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingKeywords
        fields = ['keyword']

class PopularCategoriesSerializer(serializers.ModelSerializer):
    num_posts = serializers.IntegerField(read_only=True)

    class Meta:
        model = Industry
        fields= ['name', 'num_posts']


class TopSkillSerializer(serializers.ModelSerializer):
    skills_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Industry
        fields= ['name', 'skills_count']

class PopularJobSerializer(serializers.ModelSerializer):
    favourite_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields= ['title','favourite_count']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
