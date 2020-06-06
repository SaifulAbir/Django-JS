from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from job.models import Company
from job.serializers import CompanySerializer

class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer

@api_view(["GET"])
def get_company_by_name(request):
    limit = int(request.GET.get('limit', 10))
    comp_name = request.GET.get('name')
    if comp_name:
        comps = Company.objects.filter(name__icontains=comp_name).order_by('name')[:limit]
    else:
        comps = Company.objects.all().order_by('name')[:limit]
    data = CompanySerializer(comps, many=True).data
    return Response(data)

