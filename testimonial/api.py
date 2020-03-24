from .models import Testimonial
from .serializers import TestimonialSerializer
# from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics


class TestimonialList(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer