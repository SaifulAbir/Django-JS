from rest_framework import serializers
from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency
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
    class Meta:
        model = Job
        fields = '__all__'

class JobSerializerAllField(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'salary_min']
        #fields = '__all__'

class CompanyPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'web_address', 'company_profile']
