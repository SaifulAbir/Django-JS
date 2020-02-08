from rest_framework import serializers
from .models import Division, District

class DistrictNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['name']

class DivisionSerializer(serializers.ModelSerializer):
    district = DistrictNameSerializer(many=True)
    class Meta:
        model = Division
        fields = ['name', 'district']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['name', 'division']

