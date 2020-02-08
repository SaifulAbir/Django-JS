from rest_framework import serializers
from .models import Division, District


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['division','name']
