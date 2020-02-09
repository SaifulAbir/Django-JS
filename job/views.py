from rest_framework.views import APIView
from .models import Company
from rest_framework.response import Response
from rest_framework import generics

#
# class CompanyList(APIView):
#     def get(self, request):
#         company = Company.objects.all()
#         serializer = CompanySerializer(Company)
#         return Response({"company": serializer.data})


# class CompanyList(generics.ListCreateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
