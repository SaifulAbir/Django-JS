from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from job.models import Company
from job.serializers import CompanySerializer


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@api_view(["GET"])
def get_company_by_name(request, limit=10):
    comp_name = request.GET.get('name')
    if comp_name:
        comps = Company.objects.filter(name__icontains=comp_name)[:limit]
    data = CompanySerializer(comps, many=True).data
    return Response(data)