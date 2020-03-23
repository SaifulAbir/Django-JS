from .models import Testimonial
from .serializers import DivisionSerializer, DistrictPopulateSerializer
# from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics


class TestimonialList(generics.ListAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer