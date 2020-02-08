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

class District(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

@api_view(["GET"])
def district_list(request, division):
    try:
        district_obj = District.objects.filter(division=division).order_by('-id')
        district_list = DistrictNameSerializer(district_obj)
    except District.DoesNotExist:
        district_list = []

    data = {
        'status': 'success',
        'code': HTTP_200_OK,
        "data": {
            "district_list": district_list.data,
        }
    }
    return Response(data, HTTP_200_OK)

