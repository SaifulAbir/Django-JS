from rest_framework import generics

from career_advice.models import *
from career_advice.serializers import CareerAdviceSerializer


class CareerAdviseShow(generics.ListCreateAPIView):
    queryset = CareerAdvice.objects.filter().order_by('-created_date')[:3]
    serializer_class = CareerAdviceSerializer