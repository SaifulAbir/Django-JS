from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

from job.models import Company
from .models import Division
from .models import District
from .serializers import DivisionSerializer, DistrictPopulateSerializer, DistrictSerializer
# from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics


class DivisionListCreate(generics.ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

# class DivisionUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Division.objects.all()
#     serializer_class = DivisionSerializer
#
# class DistrictList(generics.ListCreateAPIView):
#     queryset = District.objects.all()
#     serializer_class = DistrictSerializer

# @api_view(["POST"])
# def company_create(request):
#     company_data = json.loads(request.body)
#     # print(company_data['name'])
#     # company_obj = Company()
#     # company_obj.load_data(company_data)
#     # company_obj = Company(name=company_data['name'], division_id=company_data['division'], district_id=company_data['district'], address=company_data['address'])
#     company_obj = Company(**company_data)
#     company_obj.save()
#     return Response(HTTP_200_OK)

# class CompanyUpdateView(GenericAPIView, UpdateModelMixin):
#     '''
#     You just need to provide the field which is to be modified.
#     '''
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)


class DistrictPopulate(generics.ListAPIView):
    serializer_class = DistrictPopulateSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = District.objects.all()
        division = self.kwargs['division']
        print(division)
        if division is not None:
            queryset = queryset.filter(division=division)
            print(queryset)
        return queryset

class DistrictShow(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer