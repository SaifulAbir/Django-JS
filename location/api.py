from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK

from .models import Division
from .models import District
from .serializers import DivisionSerializer, DistrictNameSerializer
from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics


class DivisionListCreate(generics.ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class DivisionUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class Districtlist(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

@api_view(["GET"])
def district_list(request, division):
    try:
        district_obj = District.objects.all()
        district_list = DistrictSerializer(district_obj)
    except District.DoesNotExist:
        district_list = []

    data = {
        'status': 'success',
        'code': HTTP_200_OK,
        "data": {
            "district_list": district_list,
        }
    }
    return Response(data, HTTP_200_OK)


