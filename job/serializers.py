from rest_framework import serializers
from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill, JobSource, JobCategory, JobGender
from rest_framework.validators import *


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, label='company_name')
    # contact_no = serializers.CharField(required=True, max_length=11)
    email = serializers.CharField(max_length=30, validators=[UniqueValidator(queryset=Company.objects.all())])

    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {'client': {'required': False}}


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

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
        # TODO : Remove fields not needed
        fields = ('title','status' ,'company_name', 'address','job_category','application_deadline' ,
         'job_gender','vacancy','experience' ,
         'salary','salary_min','salary_max','currency' ,
        'description','responsibilities','education','qualification',
        'additional_requirements','other_benefits',
         'job_area','job_city','job_country' ,'company_profile',
         'company_area','company_city','company_country' ,
         'job_site','job_nature','job_type' ,'job_skills',
         'job_source_1','job_url_1' ,
         'job_source_2','job_url_2' ,
         'job_source_3','job_url_3' ,
         'created_by','created_at','modified_by','modified_at' ,
         'post_date','review_date','approve_date','publish_date' ,
         'slug', 'applied_count', 'favorite_count', 'is_applied' )



class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = ['name']

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['name']

class JobGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobGender
        fields = ['name']

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
        model = Skill
        fields= '__all__'

class PopularJobSerializer(serializers.ModelSerializer):
    favourite_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields= ['title','favourite_count']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
