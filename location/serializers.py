from rest_framework import serializers
from .models import Division, District

# class DistrictNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = District
#         fields = ['name']
#
class DistrictPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['name']

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['name']

# class DistrictSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = District
#         fields = ['name']

