from rest_framework import generics
from .models import CareerAdvice
from .test_serializers import CareerAdviseSerializer


class CareerAdviceshow(generics.ListCreateAPIView):
    queryset = CareerAdvice.objects.order_by('-created_date')[:3]
    serializer_class = CareerAdviseSerializer
