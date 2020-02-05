
from .models import Division
from .models import District
from .serializers import DivisionSerializer
from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics


class DivisionListCreate(generics.ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class DivisionUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class District(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

