from .models import CareerAdvice
from rest_framework import serializers


class CareerAdviseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerAdvice
        fields = '__all__'
