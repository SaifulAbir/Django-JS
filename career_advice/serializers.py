from rest_framework import serializers
from career_advice.models import *

class CareerAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerAdvice
        fields = '__all__'