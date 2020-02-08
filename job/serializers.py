from rest_framework import serializers
from .models import Company,Job


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'division', 'district',]



class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['name', 'industry', 'job_type','job_location', 'experience',]